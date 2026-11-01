---
name: video-production-master
description: Master skill - tổng hợp 20 libraries tạo video professional
---

# Video Production Master Skill

Skill tổng hợp 20 libraries. AI dùng file này để understand toàn bộ pipeline.

## Pipeline Overview (Master Voice & Whisper Timeline Architecture)

```
1. Script → Phân rã 5 giai đoạn, xóa emotion tags
2. Master Voice → VieNeu-TTS v3 Turbo (Đọc liền mạch 1 lần duy nhất, Zero Drift)
3. Timeline Extraction → Faster-Whisper (Trích xuất word timestamps mili-giây & phân ranh giới cảnh)
4. Visual Prompts & Storyboard → Google Flow 0 credit (Định danh @stickman, lưới chuyển động 4 ô)
5. Watermark Removal → Reverse Alpha Blending 100% sạch (Zero zoom, zero crop)
6. 60FPS Video Rendering → Remotion Studio (Spring camera physics, kinetic subtitles, ducking -22dB)
7. Video Assembly & SEO Kit → FFmpeg + generate_video_seo.py (Timestamps chuẩn Key Moments)
```

## Libraries Map

### I. Core Video (Remotion)
- **remotion-video**: React → MP4
- **motion-canvas-typescript**: TypeScript alternative

### II. Design Layer
- **satori-svg-generator**: HTML → SVG
- **svgo-optimizer**: Compress SVG

### III. Animation (5 libraries)
- **gsap-animation**: Timeline, power
- **motion-ai**: React declarative
- **animejs-lightweight**: Simple, flexible
- **rive-interactive**: State machines
- **lottie-after-effects**: Designer export

### IV. 3D Pipeline (5 libraries)
- **threejs-3d**: Core 3D
- **drei-helpers-r3f**: R3F helpers
- **rapier-physics**: Collision, gravity
- **postprocessing-effects**: Bloom, DOF

### V. Audio
- **howler-audio**: Playback, sync
- **whisper-srt-extraction**: Speech → SRT

### VI. Automation
- **gemini-api-free**: Script generation
- **youtube-api-upload**: Auto publish
- **ffmpeg-video-assembly**: Final export

## Scene Generation Pattern

```jsx
// 1. Import libraries
import {AbsoluteFill, useCurrentFrame, interpolate, Sequence} from 'remotion';
import {motion} from 'framer-motion';
import gsap from 'gsap';
import {Canvas} from '@react-three/fiber';
import {Text, Float, Environment} from '@react-three/drei';

// 2. Build scene
export const Scene = ({text, startFrame, duration}) => {
  const frame = useCurrentFrame();
  const localFrame = frame - startFrame;
  
  // Animation: fade + scale
  const opacity = interpolate(localFrame, [0, 15], [0, 1]);
  const scale = interpolate(localFrame, [0, 30], [0.8, 1]);
  
  return (
    <AbsoluteFill style={{opacity, transform: `scale(${scale})`}}>
      {/* 2D Layer */}
      <div style={{background: '#1a1a1a', width: '100%', height: '100%'}}>
        <motion.h1
          initial={{y: 50}}
          animate={{y: 0}}
          transition={{duration: 0.5}}
        >
          {text}
        </motion.h1>
      </div>
      
      {/* 3D Layer (optional) */}
      <Canvas style={{position: 'absolute', top: 0}}>
        <Environment preset="sunset" />
        <Float>
          <Text fontSize={1} color="white">
            {text}
          </Text>
        </Float>
      </Canvas>
    </AbsoluteFill>
  );
};
```

## When to Use What

**Text animations**: Motion, GSAP
**Complex timelines**: GSAP timeline
**Designer assets**: Lottie, Rive
**3D objects**: Three.js + Drei
**Physics**: Rapier (bounce, fall)
**Postprocessing**: Bloom, DOF cho polish
**Simple shapes**: SVG + Satori
**Audio sync**: Howler.js hoặc Remotion Audio

## Complexity Levels

**Simple** (text + 2D):
- Remotion + Motion
- Satori SVG backgrounds

**Medium** (animated objects):
- + GSAP timelines
- + Lottie/Rive assets

**Advanced** (3D scenes):
- + Three.js + Drei
- + Postprocessing effects

**Expert** (physics/interactive):
- + Rapier physics
- + Complex state machines

## Best Practices

1. Start simple, add complexity khi cần
2. Preload all assets
3. Keep animations < 0.5s
4. 30 FPS standard
5. Test render early
6. Profile performance
7. Use caching
8. Modular scenes
9. Reusable components
10. Document custom patterns
