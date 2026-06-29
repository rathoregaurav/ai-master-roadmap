import asyncio
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="SSE AI Example")


class PromptRequest(BaseModel):
    prompt: str


async def token_stream(prompt: str) -> AsyncIterator[str]:
    words = f"Streaming response for prompt: {prompt}".split()
    for word in words:
        await asyncio.sleep(0.2)
        yield f"data: {word}\n\n"
    yield "event: done\ndata: complete\n\n"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/stream")
async def stream(prompt: str) -> StreamingResponse:
    return StreamingResponse(token_stream(prompt), media_type="text/event-stream")

