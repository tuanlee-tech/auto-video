import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { CompositionProps } from './types';
import { CinematicSlide } from './components/CinematicSlide';
import { VideoAssetScene } from './components/VideoAssetScene';
import { KineticSubtitles } from './components/KineticSubtitles';
import { BackgroundMusic } from './components/BackgroundMusic';

const TRANSITION_FRAMES = 18; // 0.3s cross-dissolve overlap at 60fps

export const MainComposition: React.FC<CompositionProps> = ({ manifest }) => {
  if (!manifest || !manifest.scenes || manifest.scenes.length === 0) {
    return (
      <AbsoluteFill
        style={{
          backgroundColor: '#0a0a0f',
          justifyContent: 'center',
          alignItems: 'center',
          color: '#ffffff',
          fontSize: 40,
        }}
      >
        Waiting for manifest data...
      </AbsoluteFill>
    );
  }

  // Pre-calculate cumulative frame start positions dynamically
  let currentFrameAccumulator = 0;
  const scenesWithOffsets = manifest.scenes.map((scene) => {
    const from = currentFrameAccumulator;
    currentFrameAccumulator += scene.duration_frames;
    return {
      ...scene,
      from,
    };
  });

  const totalScenes = scenesWithOffsets.length;

  return (
    <AbsoluteFill style={{ backgroundColor: '#000000' }}>
      {/* Background Music Layer: Audio Ducking & Dual Mood Crossfade */}
      <BackgroundMusic
        manifest={manifest}
        totalDurationFrames={currentFrameAccumulator}
        scenesWithOffsets={scenesWithOffsets}
      />

      {/* 1. VISUAL LAYER: Cross-dissolving Slides and Videos */}
      {scenesWithOffsets.map((scene, index) => {
        const isFirst = index === 0;
        const isLast = index === totalScenes - 1;

        // Visual duration extends into the next scene's start for smooth cross-dissolve
        const visualDuration = isLast
          ? scene.duration_frames
          : scene.duration_frames + TRANSITION_FRAMES;

        return (
          <Sequence
            from={scene.from}
            durationInFrames={visualDuration}
            key={`visual-scene-${scene.scene_id}-${index}`}
          >
            {scene.asset_type === 'video' && scene.asset_file ? (
              <VideoAssetScene
                videoFile={scene.asset_file}
                durationInFrames={visualDuration}
                isFirst={isFirst}
                isLast={isLast}
                transitionFrames={TRANSITION_FRAMES}
                startOffsetSec={scene.video_start_offset_sec ?? 0}
              />
            ) : (
              <CinematicSlide
                imageFile={scene.asset_file}
                durationInFrames={visualDuration}
                motionType={scene.camera_motion}
                index={index}
                isFirst={isFirst}
                isLast={isLast}
                transitionFrames={TRANSITION_FRAMES}
              />
            )}
          </Sequence>
        );
      })}

      {/* 2. AUDIO LAYER: Continuous Single Master Voiceover */}
      {manifest.audio_file ? (
        <Audio src={staticFile(`project_assets/audio/${manifest.audio_file}`)} />
      ) : (
        scenesWithOffsets.map((scene, index) => {
          const audioSrc = scene.audio_file
            ? staticFile(`project_assets/audio/${scene.audio_file}`)
            : null;

          if (!audioSrc) return null;

          return (
            <Sequence
              from={scene.from}
              durationInFrames={scene.duration_frames}
              key={`audio-scene-${scene.scene_id}-${index}`}
            >
              <Audio src={audioSrc} />
            </Sequence>
          );
        })
      )}

      {/* 3. SUBTITLE LAYER: Calm Stationary Container with Karaoke Active-Speech Highlighting */}
      {scenesWithOffsets.map((scene, index) => {
        if (!scene.spoken_text) return null;

        return (
          <Sequence
            from={scene.from}
            durationInFrames={scene.duration_frames}
            key={`sub-scene-${scene.scene_id}-${index}`}
          >
            <KineticSubtitles
              text={scene.spoken_text}
              wordsTiming={scene.words}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
