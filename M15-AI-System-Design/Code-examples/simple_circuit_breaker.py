from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CircuitBreaker:
    failure_threshold: int = 3
    failures: int = 0
    is_open: bool = False

    def record_success(self) -> None:
        self.failures = 0
        self.is_open = False

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.is_open = True

    def allow_request(self) -> bool:
        return not self.is_open


def call_primary_model(should_fail: bool) -> str:
    if should_fail:
        raise RuntimeError("primary model unavailable")
    return "primary model answer"


def call_with_fallback(breaker: CircuitBreaker, should_fail: bool) -> str:
    if not breaker.allow_request():
        return "fallback model answer"
    try:
        result = call_primary_model(should_fail)
        breaker.record_success()
        return result
    except RuntimeError:
        breaker.record_failure()
        return "fallback model answer"


if __name__ == "__main__":
    breaker = CircuitBreaker()
    for attempt in range(5):
        print(attempt, call_with_fallback(breaker, should_fail=True), breaker)

