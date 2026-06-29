from __future__ import annotations

import statistics
import time


def fake_rag_request() -> str:
    time.sleep(0.03)
    return "answer"


def benchmark(iterations: int = 20) -> dict[str, float]:
    latencies = []
    for _ in range(iterations):
        start = time.perf_counter()
        fake_rag_request()
        latencies.append((time.perf_counter() - start) * 1000)

    sorted_latencies = sorted(latencies)
    p95_index = int(0.95 * (len(sorted_latencies) - 1))
    return {
        "count": float(iterations),
        "avg_ms": round(statistics.mean(latencies), 2),
        "p50_ms": round(statistics.median(latencies), 2),
        "p95_ms": round(sorted_latencies[p95_index], 2),
    }


if __name__ == "__main__":
    print(benchmark())

