# M1 Python for AI - Projects

> Practice projects for Python AI engineering skills.

## Project Ideas

### 1. Async LLM Batch Processor
Build a script that processes multiple prompts through an LLM API concurrently using `asyncio` and `httpx.AsyncClient`.

**Skills:** Async/await, concurrency, error handling, rate limiting

### 2. Pydantic Data Validator
Create a data validation service that validates JSON inputs/outputs for AI applications using Pydantic v2.

**Skills:** Pydantic models, field validators, custom types, serialization

### 3. Logging & Monitoring Utility
Build a logging utility using Loguru that captures structured logs for AI API calls (request ID, latency, tokens, cost).

**Skills:** Loguru, structured logging, context variables, log rotation

### 4. Type-Safe AI Client Wrapper
Create a typed wrapper around an LLM API that provides type hints, Pydantic validation, retries, and timeouts.

**Skills:** Type hints, Pydantic, httpx, retry patterns

## Starter Template

```python
# async_batch_processor.py
import asyncio
import httpx
from pydantic import BaseModel
from typing import List
import time

class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 512

class PromptResponse(BaseModel):
    text: str
    tokens_used: int
    latency_ms: float

async def process_single(client: httpx.AsyncClient, request: PromptRequest) -> PromptResponse:
    start = time.time()
    response = await client.post(
        "https://api.openai.com/v1/chat/completions",
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": request.prompt}],
            "max_tokens": request.max_tokens
        }
    )
    latency = (time.time() - start) * 1000
    data = response.json()
    return PromptResponse(
        text=data["choices"][0]["message"]["content"],
        tokens_used=data["usage"]["total_tokens"],
        latency_ms=latency
    )

async def batch_process(prompts: List[str]) -> List[PromptResponse]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [process_single(client, PromptRequest(prompt=p)) for p in prompts]
        return await asyncio.gather(*tasks, return_exceptions=True)

# Usage
results = asyncio.run(batch_process(["Hello", "What is AI?", "Tell me a joke"]))
for r in results:
    if isinstance(r, Exception):
        print(f"Failed: {r}")
    else:
        print(f"Response ({r.latency_ms:.0f}ms, {r.tokens_used} tokens): {r.text[:50]}...")