from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    user_id: str = Field(min_length=3)
    task: Literal["summarize", "classify", "extract"]
    text: str = Field(min_length=20, max_length=10_000)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)

    @field_validator("text")
    @classmethod
    def reject_empty_meaning(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned.split()) < 4:
            raise ValueError("text must contain enough natural language content")
        return cleaned


class PromptResponse(BaseModel):
    task: str
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)
    model: str


if __name__ == "__main__":
    request = PromptRequest(
        user_id="user_123",
        task="summarize",
        text="Pydantic validates data before it enters the core AI workflow.",
    )
    print(request.model_dump())

