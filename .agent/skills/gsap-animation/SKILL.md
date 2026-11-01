---
name: gsap-animation
description: GSAP timeline animations - mượt, powerful, pro-level
---

# GSAP Animation Mastery

GSAP = timeline animation engine. Mượt nhất, control tốt nhất.

## Basic Tweens

```jsx
import gsap from 'gsap';
import {useEffect, useRef} from 'react';

const box = useRef();

useEffect(() => {
  gsap.to(box.current, {
    x: 100,
    duration: 1,
    ease: 'power2.out'
  });
}, []);

return <div ref={box}>Animate me</div>;
```

## Timeline

```jsx
const tl = gsap.timeline();

tl.to('.title', {opacity: 1, y: 0, duration: 0.5})
  .to('.subtitle', {opacity: 1, y: 0, duration: 0.5}, '-=0.2') // overlap
  .to('.button', {scale: 1, duration: 0.3});
```

## Remotion Integration

```jsx
import {useCurrentFrame} from 'remotion';
import {useEffect, useRef} from 'react';
import gsap from 'gsap';

export const GSAPScene = () => {
  const frame = useCurrentFrame();
  const ref = useRef();
  
  useEffect(() => {
    if (frame === 0) {
      gsap.set(ref.current, {opacity: 0, y: 50});
    }
    if (frame === 10) {
      gsap.to(ref.current, {opacity: 1, y: 0, duration: 0.5});
    }
  }, [frame]);
  
  return <div ref={ref}>Content</div>;
};
```

## Easing

```jsx
// Power curves
ease: 'power1.out'   // subtle
ease: 'power2.out'   // standard
ease: 'power4.out'   // aggressive

// Elastic
ease: 'elastic.out(1, 0.3)'

// Back (overshoot)
ease: 'back.out(1.7)'

// Bounce
ease: 'bounce.out'
```

## Stagger

```jsx
gsap.to('.item', {
  opacity: 1,
  y: 0,
  duration: 0.5,
  stagger: 0.1  // 0.1s delay giữa mỗi item
});
```

## ScrollTrigger (for web, not video)

Skip trong video rendering. Use frame-based timing thay vì scroll.

## Best Practices

- Timeline cho multi-step sequences
- `'-=0.2'` overlap animations
- `power2.out` default easing
- Stagger cho lists
- Kill tweens on unmount: `gsap.killTweensOf(ref.current)`
