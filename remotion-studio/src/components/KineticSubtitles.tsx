import React, { useMemo } from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import { WordTiming } from '../types';

interface KineticSubtitlesProps {
  text: string;
  wordsTiming?: WordTiming[];
}

export const KineticSubtitles: React.FC<KineticSubtitlesProps> = ({
  text,
  wordsTiming,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Strip any lingering emotion tags or bracketed notes
  const cleanText = useMemo(() => {
    return text.replace(/\[.*?\]/g, '').replace(/\s+/g, ' ').trim();
  }, [text]);

  const words = useMemo(() => {
    return cleanText.split(' ').filter(Boolean);
  }, [cleanText]);

  // Gentle, calm container entrance and exit (stationary - no bouncing/jumping)
  const fadeIn = interpolate(frame, [0, 6], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const fadeOut = interpolate(
    frame,
    [durationInFrames - 6, durationInFrames],
    [1, 0],
    {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }
  );
  const containerOpacity = fadeIn * fadeOut;

  // Current playhead in milliseconds for Whisper sync
  const currentTimeMs = (frame / fps) * 1000;

  // Fallback calculation if wordsTiming is not provided
  const fallbackTimings = useMemo(() => {
    if (wordsTiming && wordsTiming.length > 0) return null;
    if (words.length === 0) return [];

    const startSpeechFrame = Math.max(2, Math.round(0.04 * fps));
    const trailingFrames = Math.max(6, Math.round(0.15 * fps));
    const endSpeechFrame = Math.max(
      startSpeechFrame + words.length,
      durationInFrames - trailingFrames
    );
    const totalSpeechSpan = Math.max(1, endSpeechFrame - startSpeechFrame);

    const weights = words.map((w) => {
      const pureLetters = w.replace(/[^a-zA-ZÀ-ỹ0-9]/g, '');
      let wt = Math.max(2, pureLetters.length);
      if (/[,;:]$/.test(w)) wt += 2;
      if (/[.?!]$/.test(w)) wt += 3;
      return wt;
    });

    const totalWeight = weights.reduce((acc, curr) => acc + curr, 0);

    let accumulatedWeight = 0;
    return words.map((word, idx) => {
      const startFr =
        startSpeechFrame + (accumulatedWeight / totalWeight) * totalSpeechSpan;
      accumulatedWeight += weights[idx];
      const endFr =
        startSpeechFrame + (accumulatedWeight / totalWeight) * totalSpeechSpan;
      return {
        word,
        startMs: (startFr / fps) * 1000,
        endMs: (endFr / fps) * 1000,
      };
    });
  }, [wordsTiming, words, fps, durationInFrames]);

  // Unified items to render
  const renderItems = useMemo(() => {
    if (wordsTiming && wordsTiming.length > 0) {
      return wordsTiming.map((wt, i) => {
        const nextStartMs =
          i < wordsTiming.length - 1
            ? wordsTiming[i + 1].start_ms
            : wt.end_ms + 100;
        return {
          word: wt.word,
          startMs: wt.start_ms,
          endMs: Math.max(wt.end_ms, nextStartMs),
        };
      });
    }
    return fallbackTimings || [];
  }, [wordsTiming, fallbackTimings]);

  if (renderItems.length === 0) return null;

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 80,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 80px',
        pointerEvents: 'none',
        zIndex: 50,
      }}
    >
      {/* Calm, stationary glassmorphism container */}
      <div
        style={{
          background: 'rgba(10, 12, 18, 0.78)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          borderRadius: 18,
          border: '1px solid rgba(255, 255, 255, 0.14)',
          padding: '16px 36px',
          maxWidth: '84%',
          textAlign: 'center',
          boxShadow: '0 16px 36px rgba(0, 0, 0, 0.55)',
          opacity: containerOpacity,
        }}
      >
        <span
          style={{
            fontFamily:
              "-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif",
            fontSize: 42,
            lineHeight: 1.4,
            letterSpacing: '-0.02em',
          }}
        >
          {renderItems.map((item, i) => {
            const isPast = currentTimeMs >= item.endMs;
            const isCurrent =
              currentTimeMs >= item.startMs && currentTimeMs < item.endMs;

            let color = 'rgba(255, 255, 255, 0.35)'; // Chưa đọc tới (Future): Trắng mờ
            let textShadow = 'none';

            if (isCurrent) {
              // Đang đọc (Current): Vàng hổ phách rực rỡ + phát sáng nhẹ (giữ nguyên font-weight chống layout shift)
              color = '#FBBF24';
              textShadow =
                '0 0 16px rgba(251, 191, 36, 0.85), 0 2px 6px rgba(0, 0, 0, 0.9)';
            } else if (isPast) {
              // Đã đọc rồi (Past): Trắng sáng thuần khiết
              color = '#FFFFFF';
              textShadow = '0 2px 6px rgba(0, 0, 0, 0.7)';
            }

            return (
              <span
                key={`${item.word}-${i}`}
                style={{
                  color,
                  fontWeight: 700, // Cố định 1 font-weight duy nhất cho toàn bộ câu để triệt tiêu layout shift
                  textShadow,
                  display: 'inline-block',
                  marginRight: 10,
                  transition: 'color 0.06s ease, text-shadow 0.06s ease',
                }}
              >
                {item.word}
              </span>
            );
          })}
        </span>
      </div>
    </div>
  );
};
