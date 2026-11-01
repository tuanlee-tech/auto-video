---
name: youtube-api-upload
description: YouTube Data API v3 - upload video programmatically
---

# YouTube Data API Upload

YouTube Data API v3 = upload video + metadata.

## Setup OAuth2

```bash
# Get credentials từ Google Cloud Console
# Enable YouTube Data API v3
# Create OAuth 2.0 Client ID
```

## Get Refresh Token (One-time)

```jsx
import {google} from 'googleapis';

const oauth2Client = new google.auth.OAuth2(
  process.env.YOUTUBE_CLIENT_ID,
  process.env.YOUTUBE_CLIENT_SECRET,
  'http://localhost:3000/oauth2callback'
);

const authUrl = oauth2Client.generateAuthUrl({
  access_type: 'offline',
  scope: ['https://www.googleapis.com/auth/youtube.upload']
});

console.log('Visit:', authUrl);

// After user authorizes, exchange code for tokens
const {tokens} = await oauth2Client.getToken(code);
console.log('Refresh token:', tokens.refresh_token);
// Save refresh_token vào .env
```

## Upload Video

```jsx
import {google} from 'googleapis';
import fs from 'fs';

const oauth2Client = new google.auth.OAuth2(
  process.env.YOUTUBE_CLIENT_ID,
  process.env.YOUTUBE_CLIENT_SECRET
);

oauth2Client.setCredentials({
  refresh_token: process.env.YOUTUBE_REFRESH_TOKEN
});

const youtube = google.youtube({
  version: 'v3',
  auth: oauth2Client
});

async function uploadVideo(filePath, title, description, tags) {
  const res = await youtube.videos.insert({
    part: ['snippet', 'status'],
    requestBody: {
      snippet: {
        title: title,
        description: description,
        tags: tags,
        categoryId: '22', // People & Blogs
        defaultLanguage: 'en',
        defaultAudioLanguage: 'en'
      },
      status: {
        privacyStatus: 'public' // or 'private', 'unlisted'
      }
    },
    media: {
      body: fs.createReadStream(filePath)
    }
  });
  
  console.log('Video ID:', res.data.id);
  console.log('URL:', `https://youtube.com/watch?v=${res.data.id}`);
  return res.data;
}
```

## Add Thumbnail

```jsx
await youtube.thumbnails.set({
  videoId: videoId,
  media: {
    body: fs.createReadStream('thumbnail.jpg')
  }
});
```

## Update Video

```jsx
await youtube.videos.update({
  part: ['snippet'],
  requestBody: {
    id: videoId,
    snippet: {
      title: 'New Title',
      description: 'New Description',
      categoryId: '22'
    }
  }
});
```

## Category IDs

```
1: Film & Animation
2: Autos & Vehicles
10: Music
15: Pets & Animals
17: Sports
19: Travel & Events
20: Gaming
22: People & Blogs
23: Comedy
24: Entertainment
25: News & Politics
26: Howto & Style
27: Education
28: Science & Technology
```

## Pipeline Integration

```jsx
async function publishVideo(videoPath, metadata) {
  const {title, description, tags, thumbnail} = metadata;
  
  // 1. Upload video
  const video = await uploadVideo(videoPath, title, description, tags);
  
  // 2. Upload thumbnail
  await youtube.thumbnails.set({
    videoId: video.id,
    media: {body: fs.createReadStream(thumbnail)}
  });
  
  return `https://youtube.com/watch?v=${video.id}`;
}
```

## Best Practices

- Store refresh_token securely (.env)
- Category 22 (People & Blogs) hoặc 27 (Education)
- Tags < 500 chars total
- Description < 5000 chars
- Title < 100 chars
- Thumbnail: 1280x720, < 2MB, JPG/PNG
- privacyStatus: 'unlisted' cho test
