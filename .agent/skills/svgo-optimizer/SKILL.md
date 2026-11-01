---
name: svgo-optimizer
description: SVGO - optimize và minify SVG files
---

# SVGO SVG Optimizer

SVGO = compress SVG, remove bloat. Giảm file size.

## CLI Usage

```bash
npx svgo input.svg -o output.svg
```

## Programmatic

```jsx
import {optimize} from 'svgo';
import fs from 'fs';

const svg = fs.readFileSync('input.svg', 'utf8');

const result = optimize(svg, {
  plugins: [
    'removeDoctype',
    'removeXMLProcInst',
    'removeComments',
    'removeMetadata',
    'removeEditorsNSData',
    'cleanupAttrs',
    'mergeStyles',
    'inlineStyles',
    'minifyStyles',
    'cleanupIds',
    'removeUselessDefs',
    'cleanupNumericValues',
    'convertColors',
    'removeUnknownsAndDefaults',
    'removeNonInheritableGroupAttrs',
    'removeUselessStrokeAndFill',
    'removeViewBox',
    'cleanupEnableBackground',
    'removeHiddenElems',
    'removeEmptyText',
    'convertShapeToPath',
    'convertEllipseToCircle',
    'moveElemsAttrsToGroup',
    'moveGroupAttrsToElems',
    'collapseGroups',
    'convertPathData',
    'convertTransform',
    'removeEmptyAttrs',
    'removeEmptyContainers',
    'mergePaths',
    'removeUnusedNS',
    'sortDefsChildren',
    'removeTitle',
    'removeDesc'
  ]
});

fs.writeFileSync('output.svg', result.data);
```

## Custom Config

```jsx
const result = optimize(svg, {
  plugins: [
    {
      name: 'preset-default',
      params: {
        overrides: {
          removeViewBox: false, // Keep viewBox
          cleanupIds: false     // Keep IDs
        }
      }
    }
  ]
});
```

## Batch Processing

```jsx
import {optimize} from 'svgo';
import fs from 'fs';
import path from 'path';

const svgDir = './svgs';
const files = fs.readdirSync(svgDir).filter(f => f.endsWith('.svg'));

files.forEach(file => {
  const svg = fs.readFileSync(path.join(svgDir, file), 'utf8');
  const result = optimize(svg);
  fs.writeFileSync(path.join(svgDir, file), result.data);
});
```

## Best Practices

- Run SVGO sau khi generate từ Satori
- Keep viewBox cho responsive
- Remove metadata/comments
- Minify colors/numbers
- Test output (visual regression)
