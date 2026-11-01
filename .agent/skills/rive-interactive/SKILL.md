---
name: rive-interactive
description: Rive animations - state machines, interactive, exported from Rive app
---

# Rive Interactive Animations

Rive = design tool export animations với state machines. Interactive.

## Basic Setup

```jsx
import {useRive} from '@rive-app/react-canvas';

const {RiveComponent} = useRive({
  src: '/animations/character.riv',
  autoplay: true
});

return <RiveComponent />;
```

## State Machine Control

```jsx
const {RiveComponent, rive} = useRive({
  src: '/character.riv',
  stateMachines: 'State Machine 1',
  autoplay: true
});

// Trigger event
const handleClick = () => {
  rive?.setInputState('State Machine 1', 'Jump', true);
};

return (
  <div onClick={handleClick}>
    <RiveComponent />
  </div>
);
```

## Remotion Integration

```jsx
import {useCurrentFrame} from 'remotion';
import {useRive} from '@rive-app/react-canvas';
import {useEffect} from 'react';

export const RiveScene = () => {
  const frame = useCurrentFrame();
  const {RiveComponent, rive} = useRive({
    src: '/animation.riv',
    stateMachines: 'Timeline',
    autoplay: false
  });
  
  useEffect(() => {
    if (rive) {
      // Sync Rive time với Remotion frame
      rive.play();
      rive.pause();
      rive.seek(frame / 30); // 30fps
    }
  }, [frame, rive]);
  
  return <RiveComponent />;
};
```

## Multiple Inputs

```jsx
const {rive} = useRive({
  src: '/character.riv',
  stateMachines: 'Controller'
});

// Boolean input
rive?.setInputState('Controller', 'isWalking', true);

// Number input
rive?.setInputState('Controller', 'speed', 0.5);

// Trigger
rive?.fireEvent('Controller', 'Jump');
```

## Best Practices

- Export từ Rive app (rive.app)
- File .riv nhỏ, vector-based
- State machines cho interactivity
- Timeline mode cho linear playback
- Combine multiple Rive files cho scenes khác nhau
- Không code animation, design trong Rive app
