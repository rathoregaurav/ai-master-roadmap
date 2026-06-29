from __future__ import annotations

import time
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Span:
    name: str
    latency_ms: float
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class RequestTrace:
    request_id: str
    spans: list[Span] = field(default_factory=list)

    def add_span(self, name: str, start_time: float, metadata: dict[str, object] | None = None) -> None:
        latency_ms = (time.perf_counter() - start_time) * 1000
        self.spans.append(Span(name=name, latency_ms=round(latency_ms, 2), metadata=metadata or {}))


def fake_retrieval() -> list[str]:
    time.sleep(0.05)
    return ["chunk-1", "chunk-2"]


def fake_model_call() -> dict[str, int | str]:
    time.sleep(0.08)
    return {"answer": "RAG needs observability.", "input_tokens": 120, "output_tokens": 18}


def run_observed_request() -> RequestTrace:
    trace = RequestTrace(request_id=str(uuid4()))

    start = time.perf_counter()
    chunks = fake_retrieval()
    trace.add_span("retrieval", start, {"chunk_ids": chunks})

    start = time.perf_counter()
    model_result = fake_model_call()
    trace.add_span("model_call", start, model_result)

    return trace


if __name__ == "__main__":
    print(run_observed_request())

