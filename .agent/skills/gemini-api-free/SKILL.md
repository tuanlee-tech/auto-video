---
name: gemini-api-free
description: Google Gemini API - free tier unlimited cho script generation
---

# Google Gemini API

Gemini API = free tier unlimited. Perfect cho script generation.

## Setup

```bash
# Get API key: aistudio.google.com/apikey
```

## Basic Usage

```jsx
import {GoogleGenerativeAI} from '@google/generative-ai';

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({model: 'gemini-pro'});

const prompt = 'Write a 60-second script about personal finance basics.';
const result = await model.generateContent(prompt);
const response = result.response;
const text = response.text();

console.log(text);
```

## Streaming

```jsx
const result = await model.generateContentStream(prompt);

for await (const chunk of result.stream) {
  process.stdout.write(chunk.text());
}
```

## Chat (Multi-turn)

```jsx
const chat = model.startChat({
  history: [
    {role: 'user', parts: [{text: 'Hello'}]},
    {role: 'model', parts: [{text: 'Hi! How can I help?'}]}
  ]
});

const result = await chat.sendMessage('Tell me about investing.');
console.log(result.response.text());
```

## System Instructions

```jsx
const model = genAI.getGenerativeModel({
  model: 'gemini-pro',
  systemInstruction: 'You are a financial education expert. Keep explanations simple and under 100 words.'
});
```

## Script Generation Pattern

```jsx
async function generateScript(topic, duration = 60) {
  const model = genAI.getGenerativeModel({model: 'gemini-pro'});
  
  const prompt = `
Create a ${duration}-second educational video script about: ${topic}

Format:
[0-5s] Hook: Attention-grabbing opening
[5-15s] Problem: What issue does this address?
[15-45s] Solution: Core content, 3 key points
[45-55s] Action: What to do next
[55-60s] CTA: Subscribe/engage

Requirements:
- Conversational tone
- Simple language
- Each section = separate paragraph
- No timestamps in output, just content
`;
  
  const result = await model.generateContent(prompt);
  return result.response.text();
}
```

## Parse Sections

```jsx
function parseScript(script) {
  const sections = script.split('\n\n').filter(s => s.trim());
  
  return sections.map((text, i) => ({
    order: i,
    text: text.trim(),
    estimatedDuration: 60 / sections.length
  }));
}
```

## Best Practices

- Free tier: unlimited requests
- Model: `gemini-pro` (text), `gemini-pro-vision` (multimodal)
- Rate limits: generous, no hard cap
- Keep prompts specific
- System instruction cho consistency
- Parse output thành structured data
