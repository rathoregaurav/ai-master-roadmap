from __future__ import annotations

import os

import httpx
from pydantic import BaseModel


class LLMMessage(BaseModel):
    role: str
    content: str


class LLMRequest(BaseModel):
    model: str
    messages: list[LLMMessage]
    temperature: float = 0.2


async def call_openai_compatible_api(request: LLMRequest) -> dict:
    api_key = os.environ["OPENAI_API_KEY"]
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=request.model_dump(),
        )
        response.raise_for_status()
        return response.json()
