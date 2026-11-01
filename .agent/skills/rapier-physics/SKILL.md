---
name: rapier-physics
description: Rapier - physics engine cho R3F (collision, gravity, forces)
---

# Rapier Physics Engine

Rapier = physics cho React Three Fiber. Collision, gravity, forces.

## Setup

```jsx
import {Physics, RigidBody} from '@react-three/rapier';

<Canvas>
  <Physics gravity={[0, -9.81, 0]}>
    <Scene />
  </Physics>
</Canvas>
```

## Static Body (Floor)

```jsx
<RigidBody type="fixed">
  <mesh position={[0, -2, 0]}>
    <boxGeometry args={[10, 0.5, 10]} />
    <meshStandardMaterial color="gray" />
  </mesh>
</RigidBody>
```

## Dynamic Body (Falls)

```jsx
<RigidBody>
  <mesh position={[0, 5, 0]}>
    <sphereGeometry args={[0.5]} />
    <meshStandardMaterial color="red" />
  </mesh>
</RigidBody>
```

## Collision Groups

```jsx
<RigidBody collisionGroups={0x0001}>
  <mesh>...</mesh>
</RigidBody>

<RigidBody collisionGroups={0x0002}>
  <mesh>...</mesh>
</RigidBody>
```

## Apply Forces

```jsx
import {useRef} from 'react';
import {RigidBody} from '@react-three/rapier';

const ball = useRef();

const jump = () => {
  ball.current?.applyImpulse({x: 0, y: 5, z: 0}, true);
};

<RigidBody ref={ball}>
  <mesh onClick={jump}>
    <sphereGeometry />
    <meshStandardMaterial />
  </mesh>
</RigidBody>
```

## Collision Events

```jsx
<RigidBody
  onCollisionEnter={(e) => console.log('Hit:', e.other)}
  onCollisionExit={(e) => console.log('Left:', e.other)}
>
  <mesh>...</mesh>
</RigidBody>
```

## Remotion Integration

```jsx
import {useCurrentFrame} from 'remotion';
import {Physics, RigidBody} from '@react-three/rapier';

export const PhysicsScene = () => {
  const frame = useCurrentFrame();
  
  // Reset physics sau mỗi frame (deterministic)
  // Hoặc: let physics run naturally
  
  return (
    <Canvas>
      <Physics paused={frame === 0}>
        <RigidBody>
          <mesh position={[0, 5, 0]}>
            <sphereGeometry args={[0.5]} />
          </mesh>
        </RigidBody>
        
        <RigidBody type="fixed">
          <mesh position={[0, -2, 0]}>
            <boxGeometry args={[10, 0.5, 10]} />
          </mesh>
        </RigidBody>
      </Physics>
    </Canvas>
  );
};
```

## Best Practices

- `type="fixed"` cho static objects
- `type="dynamic"` (default) cho moving objects
- Keep body count < 100 (performance)
- Use collision groups để ignore certain collisions
- `paused={true}` để freeze physics
- Physics = heavy, dùng khi thật sự cần (bouncing balls, falling objects)
