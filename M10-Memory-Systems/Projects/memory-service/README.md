# Memory Service

> A memory service that stores, retrieves, and manages semantic, episodic, and working memory for AI agents.

## Core Architecture

```
Agent → Memory Service → Semantic Memory (facts/knowledge)
                        → Episodic Memory (past events/sessions)
                        → Working Memory (current session context)
```

## Quick Start

```python
# memory_service.py
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime

class Memory(BaseModel):
    id: str
    type: str  # "semantic", "episodic", "working"
    content: str
    metadata: dict = {}
    created_at: str = ""
    score: float = 1.0  # relevance score
    ttl_days: int = 30  # auto-eviction

class MemoryStore:
    def __init__(self):
        self._memories: List[Memory] = []
    
    def add(self, memory: Memory):
        memory.created_at = datetime.now().isoformat()
        self._memories.append(memory)
    
    def search(self, query: str, memory_type: Optional[str] = None, top_k: int = 5) -> List[Memory]:
        """Simple keyword-based memory retrieval."""
        results = []
        query_lower = query.lower()
        for m in self._memories:
            if memory_type and m.type != memory_type:
                continue
            if query_lower in m.content.lower():
                results.append(m)
        return sorted(results, key=lambda x: x.score, reverse=True)[:top_k]
    
    def evict_expired(self):
        """Remove memories past TTL."""
        now = datetime.now()
        self._memories = [
            m for m in self._memories
            if (now - datetime.fromisoformat(m.created_at)).days < m.ttl_days
        ]

# Usage
store = MemoryStore()
store.add(Memory(id="1", type="semantic", content="User prefers Python examples"))
store.add(Memory(id="2", type="episodic", content="User completed Phase 2 on Monday"))
results = store.search("Python")
print([r.content for r in results])