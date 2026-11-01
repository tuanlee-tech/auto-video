---
name: satori-svg-generator
description: Satori - HTML/JSX thành SVG, perfect cho text layouts
---

# Satori HTML→SVG Generator

Satori biến JSX thành SVG. Perfect cho text-heavy scenes.

## Basic Usage

```jsx
import satori from 'satori';
import fs from 'fs';

const svg = await satori(
  <div style={{
    backgroundColor: 'black',
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: 'white',
    fontSize: 60
  }}>
    Hello World
  </div>,
  {
    width: 1200,
    height: 630,
    fonts: [
      {
        name: 'Inter',
        data: fs.readFileSync('./fonts/Inter-Bold.ttf'),
        weight: 700,
        style: 'normal'
      }
    ]
  }
);

fs.writeFileSync('output.svg', svg);
```

## Complex Layout

```jsx
const svg = await satori(
  <div style={{
    display: 'flex',
    flexDirection: 'column',
    width: '100%',
    height: '100%',
    padding: 80,
    backgroundColor: '#1a1a1a'
  }}>
    <h1 style={{color: 'white', fontSize: 80, margin: 0}}>
      Title
    </h1>
    <p style={{color: '#888', fontSize: 40, marginTop: 20}}>
      Subtitle text here
    </p>
    <div style={{
      display: 'flex',
      gap: 20,
      marginTop: 40
    }}>
      <div style={{backgroundColor: '#3b82f6', padding: '20px 40px', borderRadius: 8}}>
        Tag 1
      </div>
      <div style={{backgroundColor: '#10b981', padding: '20px 40px', borderRadius: 8}}>
        Tag 2
      </div>
    </div>
  </div>,
  {width: 1920, height: 1080, fonts: [/*...*/]}
);
```

## Use Case: Generate Scene Images

```jsx
async function generateSceneImage(text, subtitle) {
  const svg = await satori(
    <div style={{/*...*/}}>
      <h1>{text}</h1>
      <p>{subtitle}</p>
    </div>,
    {width: 1920, height: 1080, fonts: [/*...*/]}
  );
  
  // Convert SVG to PNG if needed
  // sharp(Buffer.from(svg)).png().toFile('scene.png');
  
  return svg;
}
```

## Remotion Integration

```jsx
import {Img, staticFile} from 'remotion';

// Pre-generate SVGs, save to public/
// Then use in Remotion
<Img src={staticFile('scene-1.svg')} />
```

## Best Practices

- Flexbox layout only (no Grid)
- Load fonts synchronously
- Keep layouts simple
- Generate SVGs pre-render
- Use for text-heavy scenes
- Fallback: plain PNG from ImageFX
