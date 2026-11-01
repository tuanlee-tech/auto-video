import React from 'react';
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

interface VideoAssetSceneProps {
  videoFile: string;
  durationInFrames: number;
  isFirst?: boolean;
  isLast?: boolean;
  transitionFrames?: number;
  startOffsetSec?: number;
}

export const VideoAssetScene: React.FC<VideoAssetSceneProps> = ({
  videoFile,
  durationInFrames,
  isFirst = false,
  isLast = false,
  transitionFrames = 18,
  startOffsetSec = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const startFromFrames = Math.round((startOffsetSec || 0) * fps);

  const fadeIn = isFirst
    ? 1
    : interpolate(frame, [0, transitionFrames], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      });

  const fadeOut = isLast
    ? 1
    : interpolate(
        frame,
        [durationInFrames - transitionFrames, durationInFrames],
        [1, 0],
        {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        }
      );

  const opacity = fadeIn * fadeOut;
  const videoSrc = staticFile(`project_assets/videos/${videoFile}`);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0f',
        overflow: 'hidden',
        opacity,
      }}
    >
      <OffthreadVideo
        src={videoSrc}
        startFrom={startFromFrames}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
      />
      {/* Subtle vignette */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(ellipse at center, rgba(0,0,0,0) 70%, rgba(0,0,0,0.5) 100%)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
