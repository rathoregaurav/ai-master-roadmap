from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256


@dataclass(frozen=True)
class ExperimentAssignment:
    experiment: str
    variant: str
    prompt_version: str


def stable_bucket(user_id: str, experiment: str) -> int:
    digest = sha256(f"{experiment}:{user_id}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 100


def assign_prompt_variant(user_id: str) -> ExperimentAssignment:
    bucket = stable_bucket(user_id, "rag_prompt_test")
    if bucket < 50:
        return ExperimentAssignment("rag_prompt_test", "A", "rag_prompt_v1")
    return ExperimentAssignment("rag_prompt_test", "B", "rag_prompt_v2")


def feature_enabled(user_id: str, feature_name: str, rollout_percent: int) -> bool:
    return stable_bucket(user_id, feature_name) < rollout_percent


if __name__ == "__main__":
    print(assign_prompt_variant("user-123"))
    print(feature_enabled("user-123", "new_citation_panel", 25))

