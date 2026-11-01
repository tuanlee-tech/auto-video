---
name: howler-audio
description: Howler.js - audio playback, sync, cross-browser
---

# Howler.js Audio Engine

Howler.js = audio playback, perfect cho sync với video.

## Basic Playback

```jsx
import {Howl} from 'howler';

const sound = new Howl({
  src: ['audio.mp3'],
  volume: 0.5,
  onload: () => console.log('Loaded'),
  onend: () => console.log('Finished')
});

sound.play();
```

## Remotion Integration

```jsx
import {Audio, staticFile} from 'remotion';

// Simple approach: use Remotion's Audio
<Audio src={staticFile('voiceover.mp3')} />

// Advanced: Howler for precise control
import {useCurrentFrame} from 'remotion';
import {Howl} from 'howler';
import {useEffect, useRef} from 'react';

export const AudioScene = () => {
  const frame = useCurrentFrame();
  const soundRef = useRef();
  
  useEffect(() => {
    soundRef.current = new Howl({
      src: ['/audio.mp3'],
      preload: true
    });
    
    return () => soundRef.current?.unload();
  }, []);
  
  useEffect(() => {
    if (soundRef.current && frame === 0) {
      soundRef.current.play();
    }
  }, [frame]);
  
  return null;
};
```

## Multiple Sounds

```jsx
const sounds = {
  bgMusic: new Howl({src: ['music.mp3'], loop: true, volume: 0.3}),
  sfx1: new Howl({src: ['pop.mp3'], volume: 0.8}),
  sfx2: new Howl({src: ['whoosh.mp3'], volume: 0.6})
};

sounds.bgMusic.play();
sounds.sfx1.play();
```

## Sprite (Multiple clips in one file)

```jsx
const sound = new Howl({
  src: ['sprite.mp3'],
  sprite: {
    intro: [0, 2000],      // 0ms - 2000ms
    main: [2000, 10000],   // 2s - 12s
    outro: [12000, 2000]   // 12s - 14s
  }
});

sound.play('intro');
sound.play('main');
```

## Seek/Position

```jsx
sound.seek(10); // Jump to 10s
const pos = sound.seek(); // Get current position
```

## Fade

```jsx
sound.fade(0, 1, 1000); // Fade from 0 to 1 over 1s
```

## Best Practices

- Preload audio
- Use Remotion `<Audio>` khi không cần control đặc biệt
- Howler cho: sprites, fade, precise sync
- .mp3 cross-browser compatible
- Keep volumes < 0.8 để tránh clip
