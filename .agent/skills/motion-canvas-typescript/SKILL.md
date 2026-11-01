---
name: motion-canvas-typescript
description: Motion Canvas - animation bằng TypeScript, code-first
---

# Motion Canvas TypeScript Animation

Motion Canvas = code animation trong TypeScript. Alternative cho After Effects.

## Setup

```bash
npm create @motion-canvas@latest
```

## Basic Scene

```tsx
import {makeScene2D} from '@motion-canvas/2d';
import {Circle} from '@motion-canvas/2d/lib/components';
import {all, waitFor} from '@motion-canvas/core/lib/flow';
import {createRef} from '@motion-canvas/core/lib/utils';

export default makeScene2D(function* (view) {
  const circle = createRef<Circle>();
  
  view.add(
    <Circle
      ref={circle}
      size={100}
      fill="#e13238"
      x={-300}
    />
  );
  
  yield* all(
    circle().position.x(300, 2),
    circle().scale(2, 2)
  );
  
  yield* waitFor(1);
});
```

## Text Animation

```tsx
import {Txt} from '@motion-canvas/2d/lib/components';

view.add(
  <Txt
    text="Hello World"
    fontSize={80}
    fill="#fff"
    opacity={0}
  />
);

const text = createRef<Txt>();

yield* all(
  text().opacity(1, 1),
  text().fontSize(120, 1)
);
```

## Layout

```tsx
import {Layout, Rect} from '@motion-canvas/2d/lib/components';

view.add(
  <Layout layout direction="column" gap={20}>
    <Rect size={100} fill="#e13238" />
    <Rect size={100} fill="#3b82f6" />
    <Rect size={100} fill="#10b981" />
  </Layout>
);
```

## Timeline

```tsx
yield* all(
  circle().position.x(300, 1),
  waitFor(0.5).to(square().position.y(200, 1))
);
```

## Signals (Reactive)

```tsx
const progress = createSignal(0);

view.add(
  <Txt
    text={() => `${Math.round(progress() * 100)}%`}
    fontSize={60}
  />
);

yield* progress(1, 2); // Animate 0 -> 1 over 2s
```

## Export

```bash
npm run render -- --output video.mp4
```

## vs Remotion

**Motion Canvas**: Code-first, TypeScript, generators, timeline control
**Remotion**: React, frame-based, declarative

Use Motion Canvas khi:
- Complex timeline logic
- Math-heavy animations
- TypeScript preference

Use Remotion khi:
- React ecosystem
- Component reuse
- Simpler mental model

## Best Practices

- Generators (`function*`) cho sequences
- `createRef()` cho component control
- `all()` cho parallel animations
- Signals cho reactive values
- Export MP4 rồi import vào Remotion nếu cần combine
