from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(frozen=True)
class PromptTemplate:
    name: str
    version: str
    owner: str
    template: str
    approved: bool


@dataclass(frozen=True)
class ModelRecord:
    name: str
    risk_level: str
    cost_level: str
    approved_use_cases: list[str]


@dataclass
class AuditLog:
    events: list[dict[str, object]] = field(default_factory=list)

    def record(self, event_type: str, actor: str, details: dict[str, object]) -> dict[str, object]:
        event = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "actor": actor,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
        }
        self.events.append(event)
        return event


def create_lineage_record(source: str, transformation: str, output: str) -> dict[str, str]:
    return {
        "source": source,
        "transformation": transformation,
        "output": output,
        "created_at": datetime.utcnow().isoformat(),
    }


if __name__ == "__main__":
    prompt = PromptTemplate("rag_answer", "v1", "ai-platform", "Answer with citations: {context}", True)
    model = ModelRecord("balanced-model", "medium", "medium", ["rag", "summarization"])
    audit = AuditLog()
    print(prompt)
    print(model)
    print(audit.record("model_selected", "system", {"model": model.name, "prompt": prompt.version}))
    print(create_lineage_record("s3://docs/policy.pdf", "chunk_and_embed", "vector://chunk-123"))

