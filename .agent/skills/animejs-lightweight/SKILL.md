---
name: animejs-lightweight
description: Anime.js - lightweight JS animation, flexible targets
---

# Anime.js Lightweight Animation

Anime.js = nhẹ, flexible, animate bất cứ property nào.

## Basic

```jsx
import anime from 'animejs';
import {useEffect, useRef} from 'react';

const box = useRef();

useEffect(() => {
  anime({
    targets: box.current,
    translateX: 250,
    duration: 1000,
    easing: 'easeOutExpo'
  });
}, []);

return <div ref={box}>Box</div>;
```

## Multiple Targets

```jsx
anime({
  targets: '.item',
  translateY: [0, 20],
  opacity: [0, 1],
  delay: anime.stagger(100) // 100ms stagger
});
```

## Timeline

```jsx
const tl = anime.timeline({
  easing: 'easeOutExpo',
  duration: 750
});

tl.add({
  targets: '.title',
  translateY: [-50, 0],
  opacity: [0, 1]
})
.add({
  targets: '.subtitle',
  translateY: [-30, 0],
  opacity: [0, 1]
}, '-=600'); // overlap 600ms
```

## Keyframes

```jsx
anime({
  targets: '.box',
  keyframes: [
    {translateY: -40},
    {translateX: 250},
    {translateY: 40},
    {translateX: 0},
    {translateY: 0}
  ],
  duration: 4000,
  easing: 'easeOutElastic(1, .8)',
  loop: true
});
```

## SVG Animation

```jsx
anime({
  targets: '#path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutSine',
  duration: 1500
});
```

## Remotion Integration

```jsx
import {useCurrentFrame} from 'remotion';
import {useEffect, useRef} from 'react';
import anime from 'animejs';

export const AnimeScene = () => {
  const frame = useCurrentFrame();
  const ref = useRef();
  
  useEffect(() => {
    if (frame === 15) {
      anime({
        targets: ref.current,
        scale: [0, 1],
        opacity: [0, 1],
        duration: 500,
        easing: 'easeOutExpo'
      });
    }
  }, [frame]);
  
  return <div ref={ref}>Content</div>;
};
```

## Easing

```jsx
easing: 'easeOutExpo'      // smooth decay
easing: 'easeInOutQuad'    // symmetric
easing: 'spring(1, 80, 10, 0)' // physics-based
easing: 'easeOutElastic(1, .6)' // bounce
```

## Best Practices

- Lighter than GSAP (5KB vs 50KB)
- Good cho simple animations
- SVG path animations excellent
- Stagger built-in
- Keyframes cho complex paths
