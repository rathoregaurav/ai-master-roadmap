from __future__ import annotations

from dataclasses import dataclass


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sum(x * x for x in a) ** 0.5
    mag_b = sum(y * y for y in b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


@dataclass(frozen=True)
class VectorRecord:
    record_id: str
    text: str
    vector: list[float]
    metadata: dict[str, str]


class InMemoryVectorStore:
    def __init__(self) -> None:
        self.records: list[VectorRecord] = []

    def add(self, record: VectorRecord) -> None:
        self.records.append(record)

    def search(
        self,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, str] | None = None,
    ) -> list[tuple[float, VectorRecord]]:
        candidates = self.records
        if filters:
            candidates = [
                record
                for record in candidates
                if all(record.metadata.get(key) == value for key, value in filters.items())
            ]
        scored = [
            (cosine_similarity(query_vector, record.vector), record)
            for record in candidates
        ]
        return sorted(scored, key=lambda item: item[0], reverse=True)[:top_k]


if __name__ == "__main__":
    store = InMemoryVectorStore()
    store.add(VectorRecord("1", "RAG retrieves evidence.", [1, 0, 0], {"type": "rag"}))
    store.add(VectorRecord("2", "FastAPI serves APIs.", [0, 1, 0], {"type": "backend"}))
    print(store.search([0.9, 0.1, 0], filters={"type": "rag"}))
