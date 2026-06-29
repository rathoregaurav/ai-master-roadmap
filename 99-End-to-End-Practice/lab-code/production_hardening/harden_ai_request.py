from __future__ import annotations

import re
import sys
import time
from dataclasses import dataclass
from uuid import uuid4


INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal the system prompt",
    "bypass safety",
]


@dataclass(frozen=True)
class HardenedResult:
    request_id: str
    allowed: bool
    security_flags: list[str]
    selected_model: str
    estimated_cost: float
    latency_ms: float
    final_text: str


def scrub_pii(text: str) -> str:
    text = re.sub(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[EMAIL_REDACTED]", text)
    text = re.sub(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE_REDACTED]", text)
    return text


def detect_injection(text: str) -> list[str]:
    lowered = text.lower()
    return [pattern for pattern in INJECTION_PATTERNS if pattern in lowered]


def choose_model(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ["architecture", "debug", "agent", "security"]):
        return "strong-model"
    if any(word in lowered for word in ["summarize", "classify", "extract"]):
        return "cheap-model"
    return "balanced-model"


def estimate_cost(text: str, model: str) -> float:
    token_estimate = max(1, len(text.split()))
    price = {
        "cheap-model": 0.001,
        "balanced-model": 0.005,
        "strong-model": 0.02,
    }[model]
    return round((token_estimate / 1000) * price, 6)


def harden_request(text: str) -> HardenedResult:
    request_id = str(uuid4())
    start = time.perf_counter()
    flags = detect_injection(text)
    scrubbed = scrub_pii(text)
    model = choose_model(scrubbed)
    cost = estimate_cost(scrubbed, model)
    allowed = not flags
    final_text = "Request blocked by security guard." if not allowed else f"Processed safely: {scrubbed}"
    latency_ms = round((time.perf_counter() - start) * 1000, 2)
    return HardenedResult(
        request_id=request_id,
        allowed=allowed,
        security_flags=flags,
        selected_model=model,
        estimated_cost=cost,
        latency_ms=latency_ms,
        final_text=final_text,
    )


if __name__ == "__main__":
    user_text = " ".join(sys.argv[1:]) or "Summarize this note. Email me at user@example.com"
    print(harden_request(user_text))

