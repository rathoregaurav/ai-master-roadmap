# LLM Provider Comparison Guide

> Quick reference for major LLM providers. Covers M3.

## Provider Comparison (2026)

| Feature | OpenAI | Anthropic | Google | Cohere | Open-Source |
|---------|--------|-----------|--------|--------|-------------|
| Best Model | GPT-4o | Claude 3.5 Opus | Gemini 2.0 | Command R+ | Llama 4, DeepSeek R1 |
| Vision | ✅ | ✅ | ✅ | ❌ | ✅ |
| Tool Calling | ✅ (strong) | ✅ (strong) | ✅ | ✅ | ✅ |
| Streaming | ✅ | ✅ | ✅ | ✅ | ✅ |
| JSON Mode | ✅ | ✅ | ✅ | ✅ | Requires prompting |
| Context Window | 128K | 200K | 2M | 128K | 128K (Llama) |
| Cost (Input/Mtok) | $2.50 | $15.00 | $1.25 | $5.00 | Free (self-host) |
| Cost (Output/Mtok) | $10.00 | $75.00 | $10.00 | $15.00 | Free (self-host) |
| Data Privacy | Opt-out | Opt-out | Opt-out | Opt-out | Full control |

## When to Use Each Provider

| Use Case | Best Provider | Why |
|----------|--------------|-----|
| General RAG | GPT-4o-mini | Cheap, fast, good at structured output |
| Complex reasoning | GPT-4o / Claude 3.5 | Best at multi-step reasoning |
| Long documents | Claude 3.5 (200K ctx) | Largest context window + high accuracy |
| Code generation | Claude 3.5 / GPT-4o | Both are excellent |
| Cost-sensitive | GPT-4o-mini / Llama 3 (local) | Cheapest options |
| Data privacy required | Self-hosted (vLLM, Ollama) | Data never leaves your infra |
| Multilingual | Gemini 2.0 | Best non-English performance |
| Classification | Cohere Command R+ | Good at classification + RAG |

## API Call Patterns

### OpenAI
```python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

### Anthropic
```python
from anthropic import Anthropic
client = Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.content[0].text)
```

### Open-Source (Ollama)
```bash
ollama pull llama3.2:3b
```
```python
import httpx
response = httpx.post("http://localhost:11434/api/chat", json={
    "model": "llama3.2:3b",
    "messages": [{"role": "user", "content": "Hello"}]
})
```

## Key Differences to Know for Interviews

1. **System Prompt Handling**: OpenAI supports system prompts officially. Anthropic treats the first `user` message with `role: "system"` as system prompt.
2. **Tool Calling**: OpenAI uses `tools` parameter. Anthropic uses `tools` similarly. Both support parallel tool calls.
3. **Streaming**: OpenAI streams tokens via SSE. Anthropic streams events (message_start, content_block_delta, etc.).
4. **Vision**: OpenAI accepts `image_url` in messages. Anthropic accepts base64 images. Google Gemini handles images natively.
5. **Context Windows**: Claude 200K > GPT-4o 128K > Gemini 2M (but Gemini's 2M is less accurate at long context).