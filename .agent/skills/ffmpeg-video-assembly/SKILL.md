---
name: ffmpeg-video-assembly
description: FFmpeg - merge, convert, export final video
---

# FFmpeg Video Assembly

FFmpeg = Swiss Army knife cho video processing.

## Basic Merge (Video + Audio)

```bash
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strict experimental output.mp4
```

## Node.js Usage

```jsx
import ffmpeg from 'fluent-ffmpeg';

ffmpeg()
  .input('video.mp4')
  .input('audio.mp3')
  .outputOptions('-c:v copy')
  .outputOptions('-c:a aac')
  .save('output.mp4')
  .on('end', () => console.log('Done'))
  .on('error', (err) => console.error(err));
```

## Concat Multiple Videos

```bash
# Create file list
echo "file 'scene1.mp4'" > list.txt
echo "file 'scene2.mp4'" >> list.txt
echo "file 'scene3.mp4'" >> list.txt

# Concat
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

```jsx
import ffmpeg from 'fluent-ffmpeg';

const videos = ['scene1.mp4', 'scene2.mp4', 'scene3.mp4'];

// Concat filter
ffmpeg()
  .input(videos[0])
  .input(videos[1])
  .input(videos[2])
  .complexFilter([
    '[0:v][1:v][2:v]concat=n=3:v=1:a=0[outv]'
  ])
  .map('[outv]')
  .save('output.mp4');
```

## Add Subtitles (SRT)

```bash
ffmpeg -i video.mp4 -vf subtitles=subs.srt output.mp4
```

## Resize/Scale

```bash
ffmpeg -i input.mp4 -vf scale=1920:1080 output.mp4
```

## Change Frame Rate

```bash
ffmpeg -i input.mp4 -r 30 output.mp4
```

## Extract Audio

```bash
ffmpeg -i video.mp4 -vn -acodec copy audio.mp3
```

## Trim

```bash
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:20 -c copy output.mp4
```

## Pipeline Integration

```jsx
import ffmpeg from 'fluent-ffmpeg';

async function assembleVideo(scenes, audioPath, outputPath) {
  return new Promise((resolve, reject) => {
    const cmd = ffmpeg();
    
    // Add all scene videos
    scenes.forEach(scene => cmd.input(scene.path));
    
    // Concat filter
    const filterComplex = scenes.map((_, i) => `[${i}:v]`).join('') + 
      `concat=n=${scenes.length}:v=1:a=0[outv]`;
    
    cmd.complexFilter([filterComplex])
       .input(audioPath)
       .map('[outv]')
       .map(`${scenes.length}:a`)
       .outputOptions('-c:v libx264')
       .outputOptions('-c:a aac')
       .save(outputPath)
       .on('end', resolve)
       .on('error', reject);
  });
}
```

## Best Practices

- `-c copy` khi không cần re-encode (nhanh)
- `-c:v libx264` cho H.264 (YouTube standard)
- `-c:a aac` cho audio
- `-r 30` force 30fps
- `-vf scale=1920:1080` resize
- Concat list file > complex filter (simpler)
