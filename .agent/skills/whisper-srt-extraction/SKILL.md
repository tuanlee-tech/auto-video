---
name: whisper-srt-extraction
description: Whisper - transcribe audio thành SRT với timestamps
---

# Whisper SRT Extraction

Whisper (OpenAI) = speech-to-text với timestamps. Tạo SRT file.

## CLI Usage

```bash
# Install
pip install openai-whisper

# Transcribe
whisper audio.mp3 --model medium --output_format srt --language en
# Output: audio.srt
```

## Node.js Integration

```bash
npm install whisper-node
```

```jsx
import whisper from 'whisper-node';

const options = {
  modelName: 'base.en',
  whisperOptions: {
    language: 'en',
    gen_file_txt: false,
    gen_file_subtitle: true,
    gen_file_vtt: false,
    word_timestamps: true
  }
};

const transcript = await whisper('audio.mp3', options);
console.log(transcript);
```

## Parse SRT

```jsx
import fs from 'fs';

function parseSRT(srtPath) {
  const content = fs.readFileSync(srtPath, 'utf8');
  const blocks = content.trim().split('\n\n');
  
  return blocks.map(block => {
    const lines = block.split('\n');
    const [start, end] = lines[1].split(' --> ').map(parseTimestamp);
    const text = lines.slice(2).join(' ');
    
    return {start, end, text};
  });
}

function parseTimestamp(ts) {
  // "00:00:10,500" -> 10.5 seconds
  const [time, ms] = ts.split(',');
  const [h, m, s] = time.split(':').map(Number);
  return h * 3600 + m * 60 + s + Number(ms) / 1000;
}

// Usage
const subtitles = parseSRT('audio.srt');
// [{start: 0, end: 3.5, text: "Hello"}, ...]
```

## Convert to Frames (30fps)

```jsx
function secondsToFrames(seconds, fps = 30) {
  return Math.round(seconds * fps);
}

const scenes = subtitles.map(sub => ({
  startFrame: secondsToFrames(sub.start),
  endFrame: secondsToFrames(sub.end),
  durationInFrames: secondsToFrames(sub.end - sub.start),
  text: sub.text
}));
```

## Pipeline Integration

```jsx
import whisper from 'whisper-node';
import fs from 'fs';

async function generateSRT(audioPath) {
  // 1. Whisper transcribe
  const options = {
    modelName: 'base.en',
    whisperOptions: {
      language: 'en',
      gen_file_subtitle: true,
      word_timestamps: true
    }
  };
  
  await whisper(audioPath, options);
  
  // 2. Read generated SRT
  const srtPath = audioPath.replace(/\.\w+$/, '.srt');
  const subtitles = parseSRT(srtPath);
  
  // 3. Convert to scenes
  const scenes = subtitles.map(sub => ({
    startFrame: secondsToFrames(sub.start),
    endFrame: secondsToFrames(sub.end),
    durationInFrames: secondsToFrames(sub.end - sub.start),
    text: sub.text
  }));
  
  return scenes;
}
```

## Best Practices

- Model sizes: tiny (fast) → small → base → medium (balanced) → large (accurate)
- `base.en` cho English (nhanh hơn multilingual)
- Word timestamps cho precise sync
- Edit SRT manual nếu cần (timing/text)
- Keep sentences 1-2 lines max trong video
