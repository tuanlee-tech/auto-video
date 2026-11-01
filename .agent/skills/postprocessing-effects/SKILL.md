---
name: postprocessing-effects
description: Postprocessing - bloom, DOF, color grading cho R3F
---

# Postprocessing Effects

Postprocessing = screen effects sau render. Bloom, DOF, color grading.

## Setup

```jsx
import {EffectComposer} from '@react-three/postprocessing';

<Canvas>
  <Scene />
  <EffectComposer>
    {/* Effects here */}
  </EffectComposer>
</Canvas>
```

## Bloom

```jsx
import {Bloom} from '@react-three/postprocessing';

<EffectComposer>
  <Bloom
    intensity={1.5}
    luminanceThreshold={0.9}
    luminanceSmoothing={0.9}
  />
</EffectComposer>
```

## Depth of Field

```jsx
import {DepthOfField} from '@react-three/postprocessing';

<EffectComposer>
  <DepthOfField
    focusDistance={0.02}
    focalLength={0.05}
    bokehScale={5}
  />
</EffectComposer>
```

## Vignette

```jsx
import {Vignette} from '@react-three/postprocessing';

<EffectComposer>
  <Vignette
    offset={0.5}
    darkness={0.5}
  />
</EffectComposer>
```

## ChromaticAberration

```jsx
import {ChromaticAberration} from '@react-three/postprocessing';

<EffectComposer>
  <ChromaticAberration
    offset={[0.002, 0.002]}
  />
</EffectComposer>
```

## Color Grading

```jsx
import {ToneMapping, BrightnessContrast, HueSaturation} from '@react-three/postprocessing';
import {ToneMappingMode} from 'postprocessing';

<EffectComposer>
  <ToneMapping mode={ToneMappingMode.ACES_FILMIC} />
  <BrightnessContrast brightness={0.05} contrast={0.1} />
  <HueSaturation hue={0} saturation={0.1} />
</EffectComposer>
```

## Glitch

```jsx
import {Glitch} from '@react-three/postprocessing';
import {GlitchMode} from 'postprocessing';

<EffectComposer>
  <Glitch
    delay={[1.5, 3.5]}
    duration={[0.6, 1.0]}
    strength={[0.3, 1.0]}
    mode={GlitchMode.SPORADIC}
  />
</EffectComposer>
```

## Noise

```jsx
import {Noise} from '@react-three/postprocessing';
import {BlendFunction} from 'postprocessing';

<EffectComposer>
  <Noise
    opacity={0.02}
    blendFunction={BlendFunction.OVERLAY}
  />
</EffectComposer>
```

## Multiple Effects

```jsx
<EffectComposer>
  <Bloom intensity={1.5} luminanceThreshold={0.9} />
  <DepthOfField focusDistance={0.02} focalLength={0.05} />
  <Vignette offset={0.5} darkness={0.5} />
  <ChromaticAberration offset={[0.001, 0.001]} />
  <Noise opacity={0.02} />
</EffectComposer>
```

## Best Practices

- Bloom cho glowing objects
- DOF cho focus effect
- Vignette cho cinematic feel
- ChromaticAberration subtle (< 0.003)
- Noise cho film grain
- Order matters: Bloom → DOF → Color → Noise
- Performance: nhiều effects = slower render
