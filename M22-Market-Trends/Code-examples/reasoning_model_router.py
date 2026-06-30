"""
M22: Reasoning Model Router
============================
Route queries between standard and reasoning models
based on complexity estimation.

Key skills:
- Complexity estimation heuristics
- Cost-aware model routing
- Comparing standard vs reasoning model outputs
- Thinking budget management
"""

import json
import logging
import math
import time
from typing import Optional

import httpx
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1. Data Models
# ──────────────────────────────────────────────

class RouterDecision(BaseModel):
    """Decision about which model to use."""
    selected_model: str
    complexity_score: float
    reasoning: str
    estimated_cost_multiplier: float


class ModelResponse(BaseModel):
    """Response from any model with metadata."""
    model: str
    content: str
    latency_ms: float
    cost_estimate: float
    thinking_tokens: Optional[int] = None


class ComparisonResult(BaseModel):
    """Comparison between standard and reasoning model."""
    question: str
    complexity_score: float
    standard_response: ModelResponse
    reasoning_response: Optional[ModelResponse] = None
    router_decision: RouterDecision
    accuracy_comparison: Optional[str] = None


# ──────────────────────────────────────────────
# 2. Complexity Estimator
# ──────────────────────────────────────────────

class ComplexityEstimator:
    """
    Estimate query complexity using multiple heuristics.
    
    Higher score = more complex = better for reasoning models.
    """

    def estimate(self, query: str) -> float:
        """
        Returns 0.0 (simple) to 1.0 (very complex).
        
        Factors:
        - Length (longer = more complex)
        - Question words (why/how/compare = more complex)
        - Math/logic indicators
        - Step indicators (multi-step required)
        - Domain specificity
        """
        scores = []
        
        # 1. Length factor (up to 0.3)
        word_count = len(query.split())
        length_score = min(1.0, word_count / 100) * 0.3
        scores.append(length_score)
        
        # 2. Question type (up to 0.3)
        complex_indicators = ["why", "how", "compare", "contrast", "analyze",
                             "explain", "difference", "relationship", "impact",
                             "implications", "what if", "scenario"]
        query_lower = query.lower()
        complex_count = sum(1 for w in complex_indicators if w in query_lower)
        question_score = min(1.0, complex_count / 3) * 0.3
        scores.append(question_score)
        
        # 3. Math/logic indicators (up to 0.2)
        math_patterns = ["calculate", "solve", "equation", "formula",
                         "probability", "statistics", "derivative",
                         "integral", "proof", "theorem", "logic"]
        math_count = sum(1 for p in math_patterns if p in query_lower)
        math_score = min(1.0, math_count / 2) * 0.2
        scores.append(math_score)
        
        # 4. Multi-step indicators (up to 0.1)
        step_indicators = ["first", "then", "finally", "step", "process",
                          "pipeline", "workflow", "sequence"]
        step_count = sum(1 for s in step_indicators if s in query_lower)
        step_score = min(1.0, step_count / 3) * 0.1
        scores.append(step_score)
        
        # 5. Code presence (up to 0.1)
        code_indicators = ["def ", "class ", "function", "import ",
                          "```", "return ", "async "]
        code_count = sum(1 for c in code_indicators if c in query)
        code_score = min(1.0, code_count / 2) * 0.1
        scores.append(code_score)
        
        total = sum(scores)
        logger.debug(f"Complexity: {total:.3f} (length={length_score:.3f}, "
                    f"question={question_score:.3f}, math={math_score:.3f}, "
                    f"step={step_score:.3f}, code={code_score:.3f})")
        return total


# ──────────────────────────────────────────────
# 3. Model Router
# ──────────────────────────────────────────────

class ModelRouter:
    """
    Routes queries to appropriate models based on complexity.
    
    Strategy:
    - Simple (< 0.3): gpt-4o-mini (cheap, fast)
    - Medium (0.3-0.7): gpt-4o (balanced)
    - Complex (> 0.7): o3-mini (reasoning model)
    """

    MODEL_CONFIGS = {
        "gpt-4o-mini": {
            "cost_per_1k_input": 0.00015,
            "cost_per_1k_output": 0.0006,
            "speed": "fast",
            "reasoning": False,
        },
        "gpt-4o": {
            "cost_per_1k_input": 0.0025,
            "cost_per_1k_output": 0.01,
            "speed": "medium",
            "reasoning": False,
        },
        "o3-mini": {
            "cost_per_1k_input": 0.0011,
            "cost_per_1k_output": 0.0044,
            "speed": "slow",
            "reasoning": True,
            "thinking_budget": 5000,
        },
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.estimator = ComplexityEstimator()
        self.client = httpx.Client(timeout=120.0)

    def decide(self, query: str) -> RouterDecision:
        """Determine which model to use for this query."""
        complexity = self.estimator.estimate(query)

        if complexity > 0.7:
            model = "o3-mini"
            reason = "Complex query requiring step-by-step reasoning"
            cost_mult = 3.0
        elif complexity > 0.3:
            model = "gpt-4o"
            reason = "Moderate complexity, balanced model sufficient"
            cost_mult = 1.0
        else:
            model = "gpt-4o-mini"
            reason = "Simple query, cheap model sufficient"
            cost_mult = 0.1

        return RouterDecision(
            selected_model=model,
            complexity_score=round(complexity, 3),
            reasoning=reason,
            estimated_cost_multiplier=cost_mult,
        )

    def query(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: str = "You are a helpful AI assistant.",
    ) -> ModelResponse:
        """Send query to specified or routed model."""
        if model is None:
            decision = self.decide(prompt)
            model = decision.selected_model

        config = self.MODEL_CONFIGS.get(model, self.MODEL_CONFIGS["gpt-4o-mini"])
        
        start = time.time()
        
        request_body = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 2000,
        }

        # Add thinking budget for reasoning models
        if config.get("reasoning") and config.get("thinking_budget"):
            request_body["thinking_budget"] = config["thinking_budget"]

        response = self.client.post(
            "https://api.openai.com/v1/chat/completions",
            json=request_body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        data = response.json()

        latency = (time.time() - start) * 1000
        content = data["choices"][0]["message"]["content"]
        
        # Estimate tokens (rough: 4 chars per token)
        input_tokens = len(prompt) // 4 + len(system_prompt) // 4
        output_tokens = len(content) // 4
        cost = (input_tokens * config["cost_per_1k_input"] / 1000 +
                output_tokens * config["cost_per_1k_output"] / 1000)

        return ModelResponse(
            model=model,
            content=content,
            latency_ms=round(latency, 1),
            cost_estimate=round(cost, 6),
            thinking_tokens=data.get("thinking_tokens"),
        )

    def compare(self, query: str) -> ComparisonResult:
        """Compare standard vs reasoning model on same query."""
        decision = self.decide(query)
        complexity = decision.complexity_score

        # Always get standard response
        standard = self.query(query, model="gpt-4o")

        # Only get reasoning response if complex enough
        reasoning = None
        if complexity > 0.3:
            reasoning = self.query(query, model="o3-mini")

        # Simple accuracy comparison
        accuracy = None
        if reasoning:
            accuracy = "Reasoning model likely more accurate for complex queries" \
                if complexity > 0.7 else "Standard model likely sufficient"

        return ComparisonResult(
            question=query,
            complexity_score=complexity,
            standard_response=standard,
            reasoning_response=reasoning,
            router_decision=decision,
            accuracy_comparison=accuracy,
        )

    def close(self):
        self.client.close()


# ──────────────────────────────────────────────
# 4. Demo
# ──────────────────────────────────────────────

def demo():
    """Compare routing decisions for different query types."""
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("No OPENAI_API_KEY set. Skipping demo.")
        return

    router = ModelRouter(api_key=api_key)
    estimator = ComplexityEstimator()

    test_queries = [
        "What is the capital of France?",
        "Explain the difference between RAG and fine-tuning, including when to use each approach.",
        "Calculate the probability of getting exactly 3 heads in 5 coin flips.",
        "Write a Python function to merge two sorted arrays.",
        "What's the weather like?",
        "Design a multi-agent system that coordinates research, writing, and fact-checking for a blog post.",
    ]

    print(f"\n{'='*80}")
    print(f"{'Query':<60} {'Complexity':<12} {'Routed Model':<15}")
    print(f"{'='*80}")

    for query in test_queries:
        decision = router.decide(query)
        short_query = query[:57] + "..." if len(query) > 60 else query
        print(f"{short_query:<60} {decision.complexity_score:<12.3f} {decision.selected_model:<15}")

    print(f"\n{'='*80}")
    print("Detailed comparison for a complex query:")
    print(f"{'='*80}")

    result = router.compare(test_queries[5])
    print(f"\nComplexity: {result.complexity_score:.3f}")
    print(f"Router: {result.router_decision.reasoning}")
    print(f"Standard ({result.standard_response.model}): "
          f"${result.standard_response.cost_estimate:.6f}, "
          f"{result.standard_response.latency_ms:.0f}ms")
    if result.reasoning_response:
        print(f"Reasoning ({result.reasoning_response.model}): "
              f"${result.reasoning_response.cost_estimate:.6f}, "
              f"{result.reasoning_response.latency_ms:.0f}ms")
        print(f"Cost ratio: {result.reasoning_response.cost_estimate / result.standard_response.cost_estimate:.1f}x")
    print(f"\nAccuracy note: {result.accuracy_comparison}")

    router.close()


if __name__ == "__main__":
    demo()