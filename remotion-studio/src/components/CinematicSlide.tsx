import React from 'react';
import {
  AbsoluteFill,
  interpolate,
  useCurrentFrame,
  Img,
  staticFile,
} from 'remotion';

interface CinematicSlideProps {
  imageFile?: string;
  durationInFrames: number;
  motionType?: 'zoom_in' | 'zoom_out' | 'pan_left' | 'pan_right';
  index: number;
  isFirst?: boolean;
  isLast?: boolean;
  transitionFrames?: number;
}

export const CinematicSlide: React.FC<CinematicSlideProps> = ({
  imageFile,
  durationInFrames,
  motionType,
  index,
  isFirst = false,
  isLast = false,
  transitionFrames = 18,
}) => {
  const frame = useCurrentFrame();

  // True Cross-Dissolve:
  // Fade in at the beginning of this scene (if not the very first scene of the video)
  const fadeIn = isFirst
    ? 1
    : interpolate(frame, [0, transitionFrames], [0, 1], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      });

  // Fade out during the transition window at the end of this scene (if not the very last scene)
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

  // Cycle camera moves if not explicitly provided
  const motions = ['zoom_in', 'pan_right', 'zoom_out', 'pan_left'] as const;
  const currentMotion = motionType || motions[index % motions.length];

  let scale = 1.0;
  let translateX = 0;
  let translateY = 0;

  if (currentMotion === 'zoom_in') {
    scale = interpolate(frame, [0, durationInFrames], [1.0, 1.06], {
      extrapolateRight: 'clamp',
    });
  } else if (currentMotion === 'zoom_out') {
    scale = interpolate(frame, [0, durationInFrames], [1.06, 1.0], {
      extrapolateRight: 'clamp',
    });
  } else if (currentMotion === 'pan_right') {
    scale = 1.05;
    translateX = interpolate(frame, [0, durationInFrames], [-25, 25], {
      extrapolateRight: 'clamp',
    });
  } else if (currentMotion === 'pan_left') {
    scale = 1.05;
    translateX = interpolate(frame, [0, durationInFrames], [25, -25], {
      extrapolateRight: 'clamp',
    });
  }

  const imageSrc = imageFile
    ? staticFile(`project_assets/images/${imageFile}`)
    : '';

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0a0a0f',
        overflow: 'hidden',
        opacity,
      }}
    >
      {/* Background Image with Spring / Interpolated Ken Burns */}
      {imageFile ? (
        <Img
          src={imageSrc}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
            transformOrigin: 'center center',
          }}
        />
      ) : (
        <AbsoluteFill
          style={{
            backgroundColor: '#111827',
            justifyContent: 'center',
            alignItems: 'center',
            color: '#6b7280',
            fontSize: 32,
            fontFamily: 'sans-serif',
          }}
        >
          Scene {index + 1}
        </AbsoluteFill>
      )}

      {/* Cinematic Vignette Overlay for Depth & Focus */}
      <AbsoluteFill
        style={{
          background:
            'radial-gradient(ellipse at center, rgba(0,0,0,0) 65%, rgba(0,0,0,0.55) 100%)',
          pointerEvents: 'none',
        }}
      />
    </AbsoluteFill>
  );
};
