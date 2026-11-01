---
name: threejs-3d
description: Three.js + R3F - 3D graphics cho video scenes
---

# Three.js 3D Pipeline

Three.js trong React qua React Three Fiber (R3F).

## Basic Setup

```jsx
import {Canvas} from '@react-three/fiber';
import {OrbitControls, PerspectiveCamera} from '@react-three/drei';

<Canvas>
  <PerspectiveCamera makeDefault position={[0, 0, 5]} />
  <ambientLight intensity={0.5} />
  <pointLight position={[10, 10, 10]} />
  <mesh>
    <boxGeometry args={[1, 1, 1]} />
    <meshStandardMaterial color="hotpink" />
  </mesh>
  <OrbitControls />
</Canvas>
```

## Remotion Integration

```jsx
import {useCurrentFrame} from 'remotion';
import {Canvas, useFrame} from '@react-three/fiber';

const Box = () => {
  const frame = useCurrentFrame();
  const rotation = (frame / 30) * Math.PI * 2; // 1 vòng/giây
  
  return (
    <mesh rotation={[0, rotation, 0]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="hotpink" />
    </mesh>
  );
};

export const Scene3D = () => (
  <Canvas>
    <ambientLight intensity={0.5} />
    <pointLight position={[10, 10, 10]} />
    <Box />
  </Canvas>
);
```

## Drei Helpers

```jsx
import {
  OrbitControls,
  PerspectiveCamera,
  Environment,
  Text3D,
  Center,
  Float
} from '@react-three/drei';

<Canvas>
  <PerspectiveCamera makeDefault position={[0, 0, 5]} />
  <Environment preset="sunset" />
  
  <Float speed={2} rotationIntensity={1}>
    <Center>
      <Text3D
        font="/fonts/helvetiker_bold.json"
        size={0.5}
        height={0.2}
      >
        HELLO
        <meshNormalMaterial />
      </Text3D>
    </Center>
  </Float>
</Canvas>
```

## Physics (Rapier)

```jsx
import {Physics, RigidBody} from '@react-three/rapier';

<Canvas>
  <Physics>
    <RigidBody type="fixed">
      <mesh position={[0, -2, 0]}>
        <boxGeometry args={[10, 0.5, 10]} />
        <meshStandardMaterial color="gray" />
      </mesh>
    </RigidBody>
    
    <RigidBody>
      <mesh position={[0, 5, 0]}>
        <sphereGeometry args={[0.5]} />
        <meshStandardMaterial color="red" />
      </mesh>
    </RigidBody>
  </Physics>
</Canvas>
```

## Postprocessing Effects

```jsx
import {EffectComposer, Bloom, DepthOfField} from '@react-three/postprocessing';

<Canvas>
  <Scene />
  <EffectComposer>
    <Bloom intensity={1.5} luminanceThreshold={0.9} />
    <DepthOfField focusDistance={0.02} focalLength={0.05} />
  </EffectComposer>
</Canvas>
```

## Camera Animation

```jsx
import {useCurrentFrame} from 'remotion';
import {PerspectiveCamera} from '@react-three/drei';

const AnimatedCamera = () => {
  const frame = useCurrentFrame();
  const z = 5 - (frame / 30); // Zoom in
  
  return <PerspectiveCamera makeDefault position={[0, 0, z]} />;
};
```

## Best Practices

- `<Canvas gl={{preserveDrawingBuffer: true}}>` cho Remotion
- Drei helpers > manual setup
- Environment maps cho lighting
- Physics chỉ khi cần (heavy)
- Postprocessing cuối cùng
- Keep poly count thấp cho render speed
