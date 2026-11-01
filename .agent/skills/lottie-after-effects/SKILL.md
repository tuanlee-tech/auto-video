---
name: lottie-after-effects
description: Lottie animations - After Effects export, JSON-based
---

# Lottie After Effects Export

Lottie = After Effects animations export sang JSON. Designer-friendly.

## Basic Setup

```jsx
import Lottie from 'lottie-react';
import animationData from './animation.json';

<Lottie animationData={animationData} loop={true} />
```

## Control Playback

```jsx
import Lottie from 'lottie-react';
import {useRef} from 'react';

const lottieRef = useRef();

const handlePlay = () => lottieRef.current?.play();
const handlePause = () => lottieRef.current?.pause();
const handleStop = () => lottieRef.current?.stop();

<Lottie
  lottieRef={lottieRef}
  animationData={animationData}
  autoplay={false}
  loop={false}
/>
```

## Remotion Integration

```jsx
import {useCurrentFrame} from 'remotion';
import Lottie from 'lottie-react';
import {useEffect, useRef} from 'react';
import animationData from './animation.json';

export const LottieScene = () => {
  const frame = useCurrentFrame();
  const lottieRef = useRef();
  
  useEffect(() => {
    if (lottieRef.current) {
      const totalFrames = animationData.op; // End frame
      const progress = frame / totalFrames;
      lottieRef.current.goToAndStop(frame, true);
    }
  }, [frame]);
  
  return (
    <Lottie
      lottieRef={lottieRef}
      animationData={animationData}
      autoplay={false}
      loop={false}
    />
  );
};
```

## Segment Playback

```jsx
<Lottie
  animationData={animationData}
  initialSegment={[0, 60]} // Play frame 0-60
  loop={true}
/>
```

## Speed Control

```jsx
<Lottie
  animationData={animationData}
  speed={0.5} // Half speed
/>
```

## Where to Get Animations

- LottieFiles.com (free library)
- Export từ After Effects (Bodymovin plugin)
- Hire designer export .json

## Best Practices

- File size: optimize trong LottieFiles
- Preload JSON files
- Use segments cho long animations
- goToAndStop() cho Remotion sync
- Color override: edit JSON (complex)
