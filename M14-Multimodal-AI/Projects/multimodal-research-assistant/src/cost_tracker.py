"""
Cost Tracker for Multi-Modal Research Assistant.
Tracks token usage and estimates cost per query.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CostEntry:
    """A single cost tracking entry."""
    modality: str  # text, image, audio, ocr
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    latency_ms: float
    timestamp: datetime = field(default_factory=datetime.now)
    query_id: Optional[str] = None


class CostTracker:
    """Track and estimate costs across all modalities."""

    RATES = {
        "gpt-4o": {"input": 0.0025 / 1000, "output": 0.01 / 1000},
        "gpt-4o-mini": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},
        "o3-mini": {"input": 0.0011 / 1000, "output": 0.0044 / 1000},
        "whisper-1": {"input": 0.006 / 60, "output": 0},  # $0.006/min
        "text-embedding-3-small": {"input": 0.00002 / 1000, "output": 0},
    }

    def __init__(self):
        self.entries: list[CostEntry] = []

    def track(
        self,
        modality: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        query_id: Optional[str] = None,
    ) -> CostEntry:
        """Record a cost entry."""
        rates = self.RATES.get(model, {"input": 0, "output": 0})
        cost = (input_tokens * rates["input"]) + (output_tokens * rates["output"])

        entry = CostEntry(
            modality=modality,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=round(cost, 6),
            latency_ms=round(latency_ms, 1),
            query_id=query_id,
        )
        self.entries.append(entry)
        return entry

    def total_cost(self) -> float:
        return sum(e.estimated_cost for e in self.entries)

    def cost_by_modality(self) -> dict[str, float]:
        costs = {}
        for e in self.entries:
            costs[e.modality] = costs.get(e.modality, 0) + e.estimated_cost
        return costs

    def summary(self) -> dict:
        return {
            "total_queries": len(self.entries),
            "total_cost": round(self.total_cost(), 6),
            "by_modality": self.cost_by_modality(),
            "avg_latency_ms": round(
                sum(e.latency_ms for e in self.entries) / max(len(self.entries), 1), 1
            ),
        }