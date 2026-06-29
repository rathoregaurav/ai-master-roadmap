from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from uuid import uuid4

from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
from pydantic import BaseModel, Field

app = FastAPI(title="AI Utility Toolkit", version="0.1.0")


class StructuredPromptRequest(BaseModel):
    prompt: str = Field(min_length=5)
    output_format: str = Field(default="summary")


class StructuredPromptResponse(BaseModel):
    request_id: str
    output_format: str
    result: dict[str, str | float]


class JobRequest(BaseModel):
    name: str = Field(min_length=3)
    payload: dict[str, str] = Field(default_factory=dict)


def require_bearer_token(authorization: str | None = Header(default=None)) -> None:
    if authorization != "Bearer dev-token":
        raise HTTPException(status_code=401, detail="invalid or missing token")


async def fake_structured_ai_call(prompt: str) -> dict[str, str | float]:
    await asyncio.sleep(0.2)
    return {
        "summary": f"Structured result for: {prompt[:80]}",
        "confidence": 0.82,
    }


async def fake_token_stream(prompt: str) -> AsyncIterator[str]:
    for token in f"This is a streamed AI-style response for: {prompt}".split():
        await asyncio.sleep(0.15)
        yield f"data: {token}\n\n"
    yield "event: done\ndata: complete\n\n"


def run_background_job(job_id: str, request: JobRequest) -> None:
    logger.info("background job {} started: {}", job_id, request.model_dump())


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/prompt/structured",
    response_model=StructuredPromptResponse,
    dependencies=[Depends(require_bearer_token)],
)
async def structured_prompt(request: StructuredPromptRequest) -> StructuredPromptResponse:
    request_id = str(uuid4())
    logger.info("structured prompt {}", request_id)
    result = await fake_structured_ai_call(request.prompt)
    return StructuredPromptResponse(
        request_id=request_id,
        output_format=request.output_format,
        result=result,
    )


@app.get("/prompt/stream")
async def stream_prompt(prompt: str) -> StreamingResponse:
    return StreamingResponse(fake_token_stream(prompt), media_type="text/event-stream")


@app.post("/jobs", dependencies=[Depends(require_bearer_token)])
def create_job(request: JobRequest, background_tasks: BackgroundTasks) -> dict[str, str]:
    job_id = str(uuid4())
    background_tasks.add_task(run_background_job, job_id, request)
    return {"job_id": job_id, "status": "queued"}
