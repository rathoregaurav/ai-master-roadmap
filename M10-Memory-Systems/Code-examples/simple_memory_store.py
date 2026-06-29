from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Memory:
    memory_id: str
    kind: str
    text: str
    created_at: str


class MemoryStore:
    def __init__(self) -> None:
        self.memories: list[Memory] = []

    def add(self, kind: str, text: str) -> Memory:
        memory = Memory(
            memory_id=f"mem-{len(self.memories) + 1}",
            kind=kind,
            text=text,
            created_at=datetime.utcnow().isoformat(),
        )
        self.memories.append(memory)
        return memory

    def search(self, query: str, kind: str | None = None) -> list[Memory]:
        terms = set(query.lower().split())
        results = []
        for memory in self.memories:
            if kind and memory.kind != kind:
                continue
            if terms & set(memory.text.lower().split()):
                results.append(memory)
        return results


if __name__ == "__main__":
    store = MemoryStore()
    store.add("semantic", "User is learning AI engineering as a beginner.")
    store.add("knowledge", "RAG uses retrieval before generation.")
    print(store.search("beginner AI"))
