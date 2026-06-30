# Cost-Aware AI Router - M20 Project

> A smart routing system that directs AI queries to the most cost-effective model without sacrificing quality.

## Architecture

```
Query → Classifier → [Simple → GPT-4o-mini → Semantic Cache]
                     [Complex → GPT-4o → Response → Cost Log]
                     [Code → Claude 3.5 → Cost Tracking]
                     [Bulk → Batch Processor → Cost Report]
```

## Router Implementation

```python
# router.py
from pydantic import BaseModel
from typing import Literal, Optional
from enum import Enum

class QueryComplexity(str, Enum):
    SIMPLE = "simple"      # Fact lookup, extraction
    MODERATE = "moderate"  # Analysis, summarization
    COMPLEX = "complex"    # Reasoning, multi-step
    CODE = "code"          # Code generation

class ModelRoute(BaseModel):
    query_id: str
    model: str
    estimated_cost: float
    estimated_latency_ms: int
    complexity: QueryComplexity

class CostAwareRouter:
    def __init__(self):
        self.model_pricing = {
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},  # per 1M tokens
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
            "llama-3-70b-local": {"input": 0.05, "output": 0.15},
        }
    
    def classify_query(self, query: str) -> QueryComplexity:
        """Classify query complexity using heuristics."""
        query_lower = query.lower()
        
        # Simple classifications
        simple_keywords = ["what is", "when is", "who is", "how many", "define", "list"]
        if any(query_lower.startswith(kw) for kw in simple_keywords) and len(query) < 100:
            return QueryComplexity.SIMPLE
        
        # Code detection
        code_keywords = ["write", "function", "class", "debug", "code", "implement", "refactor"]
        if any(kw in query_lower for kw in code_keywords):
            return QueryComplexity.CODE
        
        # Complexity heuristics
        word_count = len(query.split())
        has_examples = "example" in query_lower
        has_comparison = any(w in query_lower for w in ["compare", "difference", "vs", "versus"])
        has_reasoning = any(w in query_lower for w in ["why", "explain", "analyze", "evaluate"])
        
        complexity_score = (word_count / 10) + (2 if has_examples else 0) + \
                          (3 if has_comparison else 0) + (3 if has_reasoning else 0)
        
        if complexity_score > 8:
            return QueryComplexity.COMPLEX
        elif complexity_score > 4:
            return QueryComplexity.MODERATE
        return QueryComplexity.SIMPLE
    
    def route(self, query: str, query_id: str = "") -> ModelRoute:
        """Route query to appropriate model based on complexity."""
        complexity = self.classify_query(query)
        
        if complexity == QueryComplexity.SIMPLE:
            return ModelRoute(
                query_id=query_id,
                model="gpt-4o-mini",
                estimated_cost=0.0003,
                estimated_latency_ms=500,
                complexity=complexity
            )
        elif complexity == QueryComplexity.CODE:
            return ModelRoute(
                query_id=query_id,
                model="claude-3-5-sonnet",
                estimated_cost=0.006,
                estimated_latency_ms=2000,
                complexity=complexity
            )
        elif complexity == QueryComplexity.MODERATE:
            return ModelRoute(
                query_id=query_id,
                model="gpt-4o-mini",
                estimated_cost=0.001,
                estimated_latency_ms=1500,
                complexity=complexity
            )
        else:  # COMPLEX
            return ModelRoute(
                query_id=query_id,
                model="gpt-4o",
                estimated_cost=0.01,
                estimated_latency_ms=3000,
                complexity=complexity
            )

# Usage
router = CostAwareRouter()
queries = [
    "What is the refund policy?",
    "Write a Python function to merge two sorted lists",
    "Compare the economic policies of Keynesian and Monetarist schools of thought",
]
for q in queries:
    route = router.route(q)
    print(f"Query: {q[:40]}... → {route.model} (${route.estimated_cost:.4f})")
```

## Cost Tracking Dashboard

```python
# cost_tracker.py
class CostTracker:
    def __init__(self):
        self.usage = []
    
    def log_request(self, model: str, tokens_input: int, tokens_output: int):
        pricing = {
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-4o": {"input": 2.50, "output": 10.00},
        }
        cost = (tokens_input * pricing[model]["input"] / 1_000_000) + \
               (tokens_output * pricing[model]["output"] / 1_000_000)
        self.usage.append({"model": model, "cost": cost, "timestamp": __import__('datetime').datetime.now()})
    
    def report(self):
        total = sum(u["cost"] for u in self.usage)
        by_model = {}
        for u in self.usage:
            by_model[u["model"]] = by_model.get(u["model"], 0) + u["cost"]
        return {"total_cost": total, "by_model": by_model}
```

## Project Structure

```
cost-aware-ai-router/
├── router.py              # Model routing logic
├── classifier.py          # Query complexity classification
├── cost_tracker.py        # Cost tracking and reporting
├── cache.py               # Semantic caching
├── tests/
│   ├── test_router.py
│   └── test_cost_tracker.py
├── requirements.txt
└── README.md