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

  // Split words into compact single-line phrase chunks (strictly 1 line max)
  const chunks = useMemo(() => {
    if (!renderItems || renderItems.length === 0) return [];

    const result: {
      words: typeof renderItems;
      startMs: number;
      endMs: number;
    }[] = [];

    let currentWords: typeof renderItems = [];
    let currentChars = 0;

    renderItems.forEach((item, idx) => {
      // Fix potential missing space after punctuation in word
      const formattedWord = item.word.replace(/([,.:;?!])(?=[^\s])/g, '$1 ');
      const cleanItem = { ...item, word: formattedWord };

      currentWords.push(cleanItem);
      currentChars += formattedWord.length + 1;

      const hasPunctuation = /[,.:;?!]$/.test(item.word.trim());
      const isLast = idx === renderItems.length - 1;

      // Break chunk into strictly 1-line phrase:
      // - At natural punctuation if chunk already has >= 3 words
      // - Or when chunk reaches 5 words
      // - Or when characters reach ~28-30 chars
      const shouldBreak =
        isLast ||
        (hasPunctuation && currentWords.length >= 3) ||
        currentWords.length >= 5 ||
        currentChars >= 28;

      if (shouldBreak) {
        result.push({
          words: currentWords,
          startMs: currentWords[0].startMs,
          endMs: currentWords[currentWords.length - 1].endMs,
        });
        currentWords = [];
        currentChars = 0;
      }
    });

    // Smooth out chunk boundaries so there is no gap between consecutive chunks
    for (let i = 0; i < result.length; i++) {
      if (i < result.length - 1) {
        result[i].endMs = result[i + 1].startMs;
      } else {
        result[i].endMs = Math.max(result[i].endMs, result[i].endMs + 300);
      }
    }

    return result;
  }, [renderItems]);

  // Find the currently active 1-line chunk
  const activeChunk = useMemo(() => {
    if (!chunks || chunks.length === 0) return null;
    const match = chunks.find(
      (c) => currentTimeMs >= c.startMs && currentTimeMs < c.endMs
    );
    if (match) return match;
    if (currentTimeMs < chunks[0].startMs) return chunks[0];
    return chunks[chunks.length - 1];
  }, [chunks, currentTimeMs]);

  if (!activeChunk || activeChunk.words.length === 0) return null;

  return (
    <div
      style={{
        position: 'absolute',
        bottom: 70,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '0 40px',
        pointerEvents: 'none',
        zIndex: 50,
      }}
    >
      {/* Sleek, strictly single-line glassmorphism container */}
      <div
        style={{
          background: 'rgba(10, 12, 18, 0.78)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          borderRadius: 16,
          border: '1px solid rgba(255, 255, 255, 0.14)',
          padding: '12px 32px',
          maxWidth: '85%',
          textAlign: 'center',
          boxShadow: '0 12px 32px rgba(0, 0, 0, 0.55)',
          opacity: containerOpacity,
          whiteSpace: 'nowrap',
          overflow: 'hidden',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <span
          style={{
            fontFamily:
              "-apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif",
            fontSize: 38,
            lineHeight: 1.2,
            letterSpacing: '-0.01em',
            whiteSpace: 'nowrap',
            display: 'inline-block',
          }}
        >
          {activeChunk.words.map((item, i) => {
            const isPast = currentTimeMs >= item.endMs;
            const isCurrent =
              currentTimeMs >= item.startMs && currentTimeMs < item.endMs;

            let color = 'rgba(255, 255, 255, 0.4)';
            let textShadow = 'none';

            if (isCurrent) {
              color = '#FBBF24';
              textShadow =
                '0 0 16px rgba(251, 191, 36, 0.85), 0 2px 6px rgba(0, 0, 0, 0.9)';
            } else if (isPast) {
              color = '#FFFFFF';
              textShadow = '0 2px 6px rgba(0, 0, 0, 0.7)';
            }

            return (
              <span
                key={`${item.word}-${i}`}
                style={{
                  color,
                  fontWeight: 700,
                  textShadow,
                  display: 'inline-block',
                  marginRight: 10,
                  transition: 'color 0.05s ease, text-shadow 0.05s ease',
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
