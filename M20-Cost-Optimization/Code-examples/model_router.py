from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelChoice:
    model: str
    reason: str
    estimated_cost_level: str


def route_model(task: str, context_tokens: int) -> ModelChoice:
    lowered = task.lower()
    if context_tokens > 6000:
        return ModelChoice("strong-model", "large context needs stronger reasoning", "high")
    if any(word in lowered for word in ["summarize", "classify", "extract"]):
        return ModelChoice("cheap-model", "simple structured language task", "low")
    if any(word in lowered for word in ["design", "debug", "architecture", "agent"]):
        return ModelChoice("strong-model", "complex reasoning task", "high")
    return ModelChoice("balanced-model", "general task", "medium")


def estimate_cost(input_tokens: int, output_tokens: int, price_per_1k: float) -> float:
    return round(((input_tokens + output_tokens) / 1000) * price_per_1k, 6)


if __name__ == "__main__":
    print(route_model("summarize this support ticket", context_tokens=900))
    print(estimate_cost(input_tokens=900, output_tokens=120, price_per_1k=0.01))

