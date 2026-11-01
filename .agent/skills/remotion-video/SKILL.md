---
name: remotion-video
description: Remotion video rendering - React components thành MP4
---

# Remotion Video Production

Remotion biến React code thành video. Mỗi component = 1 scene.

## Core Concepts

**Composition**: Container chính
```jsx
import {Composition} from 'remotion';

<Composition
  id="MyVideo"
  component={MyVideo}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
/>
```

**useCurrentFrame**: Animation timeline
```jsx
import {useCurrentFrame} from 'remotion';

const frame = useCurrentFrame();
const opacity = frame < 30 ? frame / 30 : 1;
```

**interpolate**: Map frame → value
```jsx
import {interpolate, useCurrentFrame} from 'remotion';

const frame = useCurrentFrame();
const scale = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp'
});
```

## Scene Pattern

```jsx
import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';

export const Scene = ({text, startFrame, duration}) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;
  
  // Fade in
  const opacity = interpolate(localFrame, [0, 15], [0, 1]);
  
  // Scale animation
  const scale = interpolate(localFrame, [0, 30], [0.8, 1]);
  
  return (
    <AbsoluteFill style={{
      backgroundColor: '#1a1a1a',
      justifyContent: 'center',
      alignItems: 'center',
      opacity,
      transform: `scale(${scale})`
    }}>
      <h1 style={{color: 'white', fontSize: 80}}>{text}</h1>
    </AbsoluteFill>
  );
};
```

## Audio Sync

```jsx
import {Audio, staticFile} from 'remotion';

<Audio src={staticFile('voiceover.mp3')} />
```

## SRT Integration

```jsx
// Parse SRT timestamps
const subtitles = [
  {start: 0, end: 90, text: "Scene 1"},
  {start: 90, end: 180, text: "Scene 2"}
];

// Render scenes theo SRT
{subtitles.map((sub, i) => (
  <Sequence from={sub.start} durationInFrames={sub.end - sub.start} key={i}>
    <Scene text={sub.text} />
  </Sequence>
))}
```

## Export

```bash
npx remotion render src/index.tsx MyVideo out/video.mp4
```

## Best Practices

- 30 FPS standard
- 1920x1080 hoặc 1080x1920 (vertical)
- Use `<Sequence>` cho multi-scene
- `<AbsoluteFill>` thay `position: absolute`
- staticFile() cho assets
- Preload fonts
