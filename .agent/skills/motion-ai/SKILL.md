---
name: motion-ai
description: Motion library cho React animations - declarative, modern
---

# Motion Animation Library

Motion (Framer Motion fork) = declarative animations cho React.

## Basic Animation

```jsx
import {motion} from 'framer-motion';

<motion.div
  initial={{opacity: 0, y: 20}}
  animate={{opacity: 1, y: 0}}
  transition={{duration: 0.5}}
>
  Content
</motion.div>
```

## Variants Pattern

```jsx
const variants = {
  hidden: {opacity: 0, scale: 0.8},
  visible: {
    opacity: 1,
    scale: 1,
    transition: {duration: 0.5}
  }
};

<motion.div
  variants={variants}
  initial="hidden"
  animate="visible"
>
  Content
</motion.div>
```

## Remotion Integration

```jsx
import {useCurrentFrame} from 'remotion';
import {motion} from 'framer-motion';

export const MotionScene = () => {
  const frame = useCurrentFrame();
  
  return (
    <motion.div
      animate={{
        opacity: frame > 10 ? 1 : 0,
        y: frame > 10 ? 0 : 50
      }}
      transition={{duration: 0.5}}
    >
      Content
    </motion.div>
  );
};
```

## Stagger Children

```jsx
const container = {
  hidden: {opacity: 0},
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: {opacity: 0, y: 20},
  visible: {opacity: 1, y: 0}
};

<motion.div variants={container} initial="hidden" animate="visible">
  <motion.div variants={item}>Item 1</motion.div>
  <motion.div variants={item}>Item 2</motion.div>
  <motion.div variants={item}>Item 3</motion.div>
</motion.div>
```

## Layout Animations

```jsx
<motion.div layout>
  {/* Content thay đổi size/position sẽ animate smooth */}
</motion.div>
```

## Exit Animations

```jsx
import {AnimatePresence, motion} from 'framer-motion';

<AnimatePresence>
  {show && (
    <motion.div
      initial={{opacity: 0}}
      animate={{opacity: 1}}
      exit={{opacity: 0}}
    >
      Content
    </motion.div>
  )}
</AnimatePresence>
```

## Easing

```jsx
transition={{
  ease: 'easeOut',        // standard
  ease: 'easeInOut',      // symmetric
  ease: [0.17, 0.67, 0.83, 0.67], // cubic-bezier
  ease: 'anticipate'      // overshoot
}}
```

## Best Practices

- Variants cho complex animations
- `layout` prop cho responsive
- AnimatePresence cho mount/unmount
- Combine với useCurrentFrame trong Remotion
- Keep transitions < 0.5s
