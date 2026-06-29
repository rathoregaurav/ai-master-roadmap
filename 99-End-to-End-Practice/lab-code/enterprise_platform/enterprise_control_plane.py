from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from hashlib import sha256
from uuid import uuid4


@dataclass(frozen=True)
class TenantRequest:
    tenant_id: str
    user_id: str
    task: str


@dataclass(frozen=True)
class PromptVersion:
    name: str
    version: str
    approved: bool


@dataclass(frozen=True)
class ModelVersion:
    name: str
    approved: bool
    cost_level: str


@dataclass
class EnterpriseControlPlane:
    prompts: dict[str, PromptVersion]
    models: dict[str, ModelVersion]
    audit_events: list[dict[str, object]] = field(default_factory=list)

    def feature_enabled(self, tenant_id: str, feature: str, rollout_percent: int) -> bool:
        digest = sha256(f"{tenant_id}:{feature}".encode("utf-8")).hexdigest()
        bucket = int(digest[:8], 16) % 100
        return bucket < rollout_percent

    def record_audit(self, event_type: str, request: TenantRequest, details: dict[str, object]) -> None:
        self.audit_events.append(
            {
                "event_id": str(uuid4()),
                "event_type": event_type,
                "tenant_id": request.tenant_id,
                "user_id": request.user_id,
                "timestamp": datetime.utcnow().isoformat(),
                "details": details,
            }
        )

    def handle_request(self, request: TenantRequest) -> dict[str, object]:
        prompt = self.prompts["rag_answer"]
        model = self.models["balanced"]
        if not prompt.approved or not model.approved:
            raise ValueError("unapproved prompt or model")

        agent_mode = self.feature_enabled(request.tenant_id, "agent_mode", 30)
        self.record_audit(
            "ai_request",
            request,
            {
                "prompt": f"{prompt.name}:{prompt.version}",
                "model": model.name,
                "agent_mode": agent_mode,
            },
        )
        lineage = {
            "source": "s3://tenant-docs/policy.pdf",
            "transformation": "retrieve_chunks",
            "output": "answer_context",
        }
        return {
            "tenant_id": request.tenant_id,
            "answer": "Enterprise AI response with governance metadata.",
            "lineage": lineage,
            "audit_count": len(self.audit_events),
        }


if __name__ == "__main__":
    control_plane = EnterpriseControlPlane(
        prompts={"rag_answer": PromptVersion("rag_answer", "v1", True)},
        models={"balanced": ModelVersion("balanced-model", True, "medium")},
    )
    print(control_plane.handle_request(TenantRequest("tenant-a", "user-1", "Explain policy")))
    print(control_plane.audit_events)

