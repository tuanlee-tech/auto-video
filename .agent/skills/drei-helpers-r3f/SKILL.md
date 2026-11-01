---
name: drei-helpers-r3f
description: Drei - helper components cho React Three Fiber
---

# Drei R3F Helpers

Drei = helper library cho R3F. Giảm boilerplate.

## Camera

```jsx
import {PerspectiveCamera, OrbitControls} from '@react-three/drei';

<Canvas>
  <PerspectiveCamera makeDefault position={[0, 0, 5]} fov={75} />
  <OrbitControls />
</Canvas>
```

## Text

```jsx
import {Text, Text3D, Center} from '@react-three/drei';

// 2D Text (billboard)
<Text
  position={[0, 0, 0]}
  fontSize={1}
  color="white"
  anchorX="center"
  anchorY="middle"
>
  Hello
</Text>

// 3D Text
<Center>
  <Text3D
    font="/fonts/helvetiker_bold.json"
    size={0.5}
    height={0.2}
  >
    3D TEXT
    <meshNormalMaterial />
  </Text3D>
</Center>
```

## Environment/Lighting

```jsx
import {Environment, ContactShadows} from '@react-three/drei';

<Canvas>
  <Environment preset="sunset" />
  {/* OR */}
  <Environment files="/hdri/sky.hdr" />
  
  <ContactShadows
    position={[0, -1, 0]}
    opacity={0.5}
    blur={2}
  />
</Canvas>
```

## Shapes

```jsx
import {Box, Sphere, Plane, RoundedBox} from '@react-three/drei';

<Box args={[1, 1, 1]}>
  <meshStandardMaterial color="hotpink" />
</Box>

<Sphere args={[1, 32, 32]}>
  <meshStandardMaterial color="blue" />
</Sphere>

<RoundedBox args={[1, 1, 1]} radius={0.1}>
  <meshStandardMaterial color="green" />
</RoundedBox>
```

## Float/Wobble

```jsx
import {Float, Wobble} from '@react-three/drei';

<Float speed={2} rotationIntensity={1} floatIntensity={2}>
  <Box />
</Float>

<Wobble factor={1} speed={2}>
  <Sphere />
</Wobble>
```

## HTML Overlay

```jsx
import {Html} from '@react-three/drei';

<mesh>
  <Html center>
    <div style={{background: 'white', padding: 10}}>
      Label
    </div>
  </Html>
</mesh>
```

## Image/Texture

```jsx
import {Image, useTexture} from '@react-three/drei';

<Image url="/texture.jpg" scale={[2, 1]} />

// OR
const texture = useTexture('/texture.jpg');
<mesh>
  <planeGeometry args={[2, 1]} />
  <meshBasicMaterial map={texture} />
</mesh>
```

## Preload

```jsx
import {Preload} from '@react-three/drei';

<Canvas>
  <Scene />
  <Preload all />
</Canvas>
```

## Best Practices

- Environment preset > manual lights
- Text over Text3D (lighter)
- Center components cho alignment
- Float/Wobble cho idle motion
- ContactShadows > real shadows (faster)
- Preload all assets
