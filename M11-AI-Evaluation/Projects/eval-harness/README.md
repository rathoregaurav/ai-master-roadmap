# Evaluation Harness - M11 Project

> A reusable evaluation framework for testing RAG, agents, and LLM outputs against golden datasets.

## Quick Start

```python
# eval_harness.py
from pydantic import BaseModel
from typing import List, Dict, Any
import json

class TestCase(BaseModel):
    query: str
    expected_answer: str
    expected_documents: List[str] = []

class EvalResult(BaseModel):
    query: str
    groundedness: float
    recall: float
    exact_match: bool
    latency_ms: float
    tokens_used: int

class EvalHarness:
    def __init__(self, golden_dataset: List[TestCase]):
        self.dataset = golden_dataset
    
    async def run(self, system_fn) -> List[EvalResult]:
        """Run all test cases through the system function."""
        import time
        results = []
        for tc in self.dataset:
            start = time.time()
            response = await system_fn(tc.query)
            latency = (time.time() - start) * 1000
            
            results.append(EvalResult(
                query=tc.query,
                groundedness=self._calc_groundedness(response, tc.expected_answer),
                recall=self._calc_recall(response, tc.expected_documents),
                exact_match=tc.expected_answer.lower() in response.lower(),
                latency_ms=latency,
                tokens_used=len(response.split())
            ))
        return results
    
    def _calc_groundedness(self, response: str, expected: str) -> float:
        """Simple word-overlap groundedness metric."""
        response_words = set(response.lower().split())
        expected_words = set(expected.lower().split())
        if not expected_words:
            return 0.0
        overlap = len(response_words & expected_words)
        return overlap / len(expected_words)
    
    def _calc_recall(self, response: str, expected_docs: List[str]) -> float:
        if not expected_docs:
            return 1.0
        found = sum(1 for doc in expected_docs if doc.lower() in response.lower())
        return found / len(expected_docs)
    
    def report(self, results: List[EvalResult]):
        """Generate summary report."""
        avg_groundedness = sum(r.groundedness for r in results) / len(results)
        avg_recall = sum(r.recall for r in results) / len(results)
        avg_latency = sum(r.latency_ms for r in results) / len(results)
        
        return {
            "total_cases": len(results),
            "avg_groundedness": round(avg_groundedness, 3),
            "avg_recall": round(avg_recall, 3),
            "avg_latency_ms": round(avg_latency, 1),
            "pass_rate": round(sum(1 for r in results if r.groundedness > 0.7) / len(results), 3)
        }
```

## Project Structure

```
eval-harness/
├── harness.py           # Core evaluation framework
├── metrics.py            # RAGAS-style metrics
├── datasets/             # Golden datasets
│   └── rag_golden.json
├── reporters/            # Report generators
│   ├── json_reporter.py
│   └── markdown_reporter.py
├── requirements.txt
└── README.md