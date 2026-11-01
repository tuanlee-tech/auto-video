---
name: browser-automation-claude
description: Claude browser tools - điều khiển Google services (ImageFX, VideoFX, Gemini TTS)
---

# Claude Browser Automation

Claude browser tools = thay Playwright. Điều khiển Chrome debug mode.

## Chrome Debug Mode

```bash
# Start Chrome với remote debugging
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome-automation" --headless=new
```

## Claude Browser Tools

```jsx
// Available tools qua Claude:
// - preview_eval: Execute JS
// - preview_click: Click element
// - preview_fill: Fill input
// - preview_inspect: Get element info
// - preview_screenshot: Take screenshot
// - preview_snapshot: Get accessibility tree
```

## Pattern: Login & Use Service

```jsx
async function useGoogleService(accountIndex) {
  // 1. Load cookies
  const account = accounts[accountIndex];
  // preview_eval to set cookies
  
  // 2. Navigate
  // preview_eval: window.location.href = 'https://imagefx.google.com'
  
  // 3. Wait for load
  // preview_snapshot to check page ready
  
  // 4. Interact
  // preview_fill prompt input
  // preview_click generate button
  
  // 5. Download result
  // preview_eval to get image blob
}
```

## ImageFX Automation

```jsx
// Navigate to ImageFX
await preview_eval(`window.location.href = 'https://imagefx.google.com'`);

// Fill prompt
await preview_fill('textarea[placeholder="Describe an image"]', prompt);

// Click generate
await preview_click('button[aria-label="Generate"]');

// Wait for result
await new Promise(r => setTimeout(r, 10000));

// Download image
const imageUrl = await preview_eval(`
  document.querySelector('img[src^="blob:"]').src
`);
```

## VideoFX Automation

```jsx
// Similar pattern
await preview_eval(`window.location.href = 'https://videofx.google.com'`);

// Upload image
await preview_fill('input[type="file"]', imagePath);

// Select duration (4s/6s/8s/10s)
await preview_click(`button[data-duration="${duration}"]`);

// Generate
await preview_click('button[aria-label="Generate video"]');

// Wait (longer cho video)
await new Promise(r => setTimeout(r, 30000));

// Download
const videoUrl = await preview_eval(`
  document.querySelector('video source').src
`);
```

## Gemini TTS Automation

```jsx
// Navigate
await preview_eval(`window.location.href = 'https://aistudio.google.com/generate-speech?model=gemini-3.8-flash-tts'`);

// Fill text
await preview_fill('textarea', scriptText);

// Select voice
await preview_click('button[data-voice="Fola"]');

// Generate
await preview_click('button[aria-label="Generate"]');

// Download audio
const audioBlob = await preview_eval(`
  // Get audio element
  const audio = document.querySelector('audio');
  audio.src;
`);
```

## Account Rotation

```jsx
class AccountManager {
  constructor(accounts) {
    this.accounts = accounts;
    this.currentIndex = 0;
  }
  
  getNext() {
    const account = this.accounts[this.currentIndex];
    this.currentIndex = (this.currentIndex + 1) % this.accounts.length;
    
    // Check daily limit
    if (account.usedToday >= account.dailyLimit) {
      // Try next account
      return this.getNext();
    }
    
    return account;
  }
  
  incrementUsage(accountId) {
    const account = this.accounts.find(a => a.id === accountId);
    account.usedToday++;
  }
  
  resetDailyLimits() {
    const today = new Date().toISOString().split('T')[0];
    this.accounts.forEach(acc => {
      if (acc.lastReset !== today) {
        acc.usedToday = 0;
        acc.lastReset = today;
      }
    });
  }
}
```

## Best Practices

- Chrome debug mode separate profile
- Cookie persistence
- Account rotation
- Rate limit tracking
- Error handling (retry different account)
- Headless = faster
- Screenshot cho debug
- Snapshot > Screenshot (accessibility tree)
