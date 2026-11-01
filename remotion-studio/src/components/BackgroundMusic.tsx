import React, { useMemo } from 'react';
import { Audio, staticFile, useVideoConfig } from 'remotion';
import { ManifestData, SceneData } from '../types';

interface BackgroundMusicProps {
  manifest: ManifestData;
  totalDurationFrames: number;
  scenesWithOffsets: (SceneData & { from: number })[];
}

export const BackgroundMusic: React.FC<BackgroundMusicProps> = ({
  manifest,
  totalDurationFrames,
  scenesWithOffsets,
}) => {
  const { fps } = useVideoConfig();

  const bgmConfig = manifest.bgm;
  const track1 = bgmConfig?.track_1 || manifest.bgm_file;
  const track2 = bgmConfig?.track_2;
  const mode = bgmConfig?.mode || (track2 ? 'dual' : 'single');

  const volDucked = bgmConfig?.volume_ducked ?? manifest.bgm_volume_ducked ?? 0.14;
  const volNormal = bgmConfig?.volume_normal ?? manifest.bgm_volume_normal ?? 0.32;
  const fadeInFrames = bgmConfig?.fade_in_frames ?? 60;
  const fadeOutFrames = bgmConfig?.fade_out_frames ?? 120;

  // 1. Precalculate speech intervals (in frames) from whisper word timestamps
  const speechIntervals = useMemo(() => {
    const intervals: { start: number; end: number }[] = [];
    const PAD_FRAMES = 10; // ~0.16s smoothing before/after speech

    scenesWithOffsets.forEach((scene) => {
      if (scene.words && scene.words.length > 0) {
        scene.words.forEach((w) => {
          const wStart = scene.from + Math.round((w.start_ms / 1000) * fps) - PAD_FRAMES;
          const wEnd = scene.from + Math.round((w.end_ms / 1000) * fps) + PAD_FRAMES;
          intervals.push({
            start: Math.max(0, wStart),
            end: Math.min(totalDurationFrames, wEnd),
          });
        });
      } else {
        // Fallback: whole scene duration
        intervals.push({
          start: scene.from,
          end: scene.from + scene.duration_frames,
        });
      }
    });

    if (intervals.length === 0) return [];
    intervals.sort((a, b) => a.start - b.start);
    const merged = [intervals[0]];
    for (let i = 1; i < intervals.length; i++) {
      const last = merged[merged.length - 1];
      const cur = intervals[i];
      if (cur.start <= last.end) {
        last.end = Math.max(last.end, cur.end);
      } else {
        merged.push(cur);
      }
    }
    return merged;
  }, [scenesWithOffsets, fps, totalDurationFrames]);

  // Determine transition frame for dual mode
  const transitionFrame = useMemo(() => {
    if (mode !== 'dual' || !track2) return totalDurationFrames;
    const transSceneId = bgmConfig?.transition_scene_id;
    if (transSceneId) {
      const match = scenesWithOffsets.find((s) => s.scene_id === transSceneId);
      if (match) return match.from;
    }
    return Math.floor(totalDurationFrames / 2);
  }, [mode, track2, bgmConfig, scenesWithOffsets, totalDurationFrames]);

  const CROSSFADE_FRAMES = 120; // 2 seconds crossfade between mood tracks

  // Dynamic volume calculator with Smooth Audio Ducking
  const getVolumeMultiplier = (f: number): number => {
    // Master fade-in & fade-out
    let masterFade = 1;
    if (f < fadeInFrames) {
      masterFade = f / Math.max(1, fadeInFrames);
    } else if (f > totalDurationFrames - fadeOutFrames) {
      masterFade = Math.max(0, (totalDurationFrames - f) / Math.max(1, fadeOutFrames));
    }

    // Audio Ducking with smooth 12-frame (0.2s) attack/release ramp
    const RAMP_FRAMES = 12;
    let duckFactor = 0; // 0 = normal (music loud), 1 = fully ducked (voice dominant)

    for (const interval of speechIntervals) {
      if (f >= interval.start && f <= interval.end) {
        duckFactor = 1;
        break;
      } else if (f >= interval.start - RAMP_FRAMES && f < interval.start) {
        const factor = (f - (interval.start - RAMP_FRAMES)) / RAMP_FRAMES;
        duckFactor = Math.max(duckFactor, factor);
      } else if (f > interval.end && f <= interval.end + RAMP_FRAMES) {
        const factor = 1 - (f - interval.end) / RAMP_FRAMES;
        duckFactor = Math.max(duckFactor, factor);
      }
    }

    const baseVol = volNormal - duckFactor * (volNormal - volDucked);
    return baseVol * masterFade;
  };

  if (!track1) return null;

  return (
    <>
      {/* Track 1 (Opening / Problem) */}
      <Audio
        src={staticFile(`project_assets/bgm/${track1}`)}
        loop
        volume={(f) => {
          const vol = getVolumeMultiplier(f);
          if (mode === 'dual' && track2) {
            if (f < transitionFrame) return vol;
            if (f >= transitionFrame + CROSSFADE_FRAMES) return 0;
            const progress = (f - transitionFrame) / CROSSFADE_FRAMES;
            return vol * (1 - progress);
          }
          return vol;
        }}
      />

      {/* Track 2 (Awakening / Resolution) */}
      {mode === 'dual' && track2 && (
        <Audio
          src={staticFile(`project_assets/bgm/${track2}`)}
          loop
          volume={(f) => {
            const vol = getVolumeMultiplier(f);
            if (f < transitionFrame) return 0;
            if (f >= transitionFrame + CROSSFADE_FRAMES) return vol;
            const progress = (f - transitionFrame) / CROSSFADE_FRAMES;
            return vol * progress;
          }}
        />
      )}
    </>
  );
};
