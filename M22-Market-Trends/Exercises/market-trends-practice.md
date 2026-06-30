# M22: Market Trends — Practice Exercises

> **Weeks 26–27 · Phase 6 · Future-Proofing & Trends**

---

## Exercise 0: Environment Setup

```bash
# For Week 26
export OPENAI_API_KEY='your-key-here'

# For Week 27 - Install Ollama
brew install ollama
ollama pull llama3.2:3b
ollama pull mistral:7b
```

---

## Week 26: Reasoning Models & Synthetic Data

### Exercise 1: Complexity Classification (15 min)

**Task:** Build a query complexity classifier.

1. Create 20 test queries of varying complexity (simple facts, multi-step analysis, math problems)
2. Run `reasoning_model_router.py` on all of them
3. Analyze the complexity scores:
   - Which queries scored >0.7?
   - Which scored <0.3?
   - Were any misclassified?

**Challenge:** Add your own complexity heuristics beyond the built-in ones.

**Success Criteria:** Your router correctly classifies at least 18/20 queries.

---

### Exercise 2: Cost-Aware Model Selection (25 min)

**Task:** Compare costs of different model strategies.

Run the same 5 queries through:
1. `gpt-4o-mini` (cheapest)
2. `gpt-4o` (balanced)
3. `o3-mini` (reasoning)
4. Your router (intelligent routing)

| Query | gpt-4o-mini | gpt-4o | o3-mini | Router |
|-------|-------------|--------|---------|--------|
| "What is 2+2?" | $— | $— | $— | $— |
| "Solve this equation..." | $— | $— | $— | $— |
| "Write a haiku" | $— | $— | $— | $— |
| "Design a distributed system..." | $— | $— | $— | $— |
| Total | $— | $— | $— | $— |

**Success Criteria:** Router saves at least 40% vs always using gpt-4o.

---

### Exercise 3: Long-Context Strategy Comparison (30 min)

**Task:** Compare 4 strategies for handling a 50-page document.

1. Create a test document (or find one) with ~50 pages
2. Implement and compare:
   - **Naive**: Throw entire document in context
   - **Sliding Window RAG**: Chunk + retrieve top 5 chunks
   - **Hierarchical Summary**: Summarize chunks → summarize summaries
   - **Hybrid**: RAG for retrieval → long-context for synthesis

| Strategy | Cost | Latency | Accuracy |
|----------|------|---------|----------|
| Naive | — | — | — |
| Sliding RAG | — | — | — |
| Hierarchical | — | — | — |
| Hybrid | — | — | — |

**Success Criteria:** Identify which strategy is best for: (a) cost, (b) latency, (c) accuracy.

---

### Exercise 4: Synthetic Data Generation (30 min)

**Task:** Generate a golden dataset for RAG evaluation.

1. Pick a topic (e.g., "MCP protocol" or "Kubernetes")
2. Use `synthetic_data_generator.py` to generate 30 Q&A pairs
3. Generate 10 adversarial examples to test boundaries
4. Validate the dataset quality (at least 5 sample checks)
5. Analyze the distribution:
   - Difficulty mix (easy/medium/hard)
   - Topic coverage
   - Adversarial edge cases

**Challenge:** Generate from a real document (e.g., a README or blog post).

**Success Criteria:** A validated golden dataset with >80% valid pairs and at least 3 difficulty levels.

---

### Exercise 5: Reasoning vs Standard Comparison (20 min)

**Task:** Find the break-even point where reasoning models become worth the cost.

1. Create a test set of 10 questions across difficulty levels
2. Run each through both standard (gpt-4o) and reasoning (o3-mini) models
3. Compare:
   - Correctness (by your judgment)
   - Cost per query
   - Latency
4. Identify: At what complexity threshold does the reasoning model start winning?

**Challenge:** Graph the cost/accuracy tradeoff curve.

**Success Criteria:** A clear recommendation: "Use reasoning model when complexity > X."

---

## Week 27: SLMs & Open Ecosystem

### Exercise 6: Local Model Setup (15 min)

**Task:** Get a local SLM running.

```bash
# Install and run
ollama pull llama3.2:3b
ollama run llama3.2:3b "Explain RAG in one sentence"

# Try another model
ollama pull mistral:7b
ollama run mistral:7b "Write a Python function to sort a list"
```

Compare the outputs. Which is faster? Which gives better answers?

**Success Criteria:** Both models running locally and you can articulate the differences.

---

### Exercise 7: SLM vs Cloud Comparison (20 min)

**Task:** Compare local SLM vs cloud LLM on classification tasks.

Create 10 classification prompts (e.g., "Classify this email as spam or not spam") and run through:

| Query | Llama 3.2 3B (local) | Mistral 7B (local) | GPT-4o-mini (cloud) |
|-------|----------------------|--------------------|--------------------|
| 1 | — | — | — |
| 2 | — | — | — |
| ... | — | — | — |
| Accuracy | —% | —% | —% |
| Cost | $0 | $0 | $— |
| Latency | —ms | —ms | —ms |

**Success Criteria:** You can articulate: "For simple classification, local is X% as accurate for Y% of the cost."

---

### Exercise 8: Hybrid SLM/Cloud Router (30 min)

**Task:** Build a hybrid router that routes simple tasks to local SLM, complex to cloud.

```python
class HybridRouter:
    def __init__(self, local_model, cloud_api):
        self.local = local_model  # Ollama
        self.cloud = cloud_api    # OpenAI
        
    def query(self, text: str, complexity: str = "auto"):
        if complexity == "simple":
            return self.local.generate(text)
        elif self._is_complex(text):
            return self.cloud.generate(text)
        else:
            return self.local.generate(text)  # Default to local
```

Test with:
- 5 simple queries (→ local)
- 5 complex queries (→ cloud)
- 5 ambiguous queries (test your `_is_complex` heuristic)

**Success Criteria:** Router saves >60% cost vs always using cloud, with <5% accuracy loss.

---

### Exercise 9: Quantization Comparison (20 min)

**Task:** Compare model quality at different quantization levels.

```bash
# Pull full precision
ollama pull llama3.2:3b

# Pull quantized version (if available)
# Compare quality on 5 test prompts
```

For each quantization level (FP16, Q4, Q2):
1. Generate the same 5 prompts
2. Rate output quality (1-5)
3. Measure response time
4. Check model size

| Quantization | Size | Quality (1-5) | Speed | RAM Usage |
|-------------|------|---------------|-------|-----------|
| FP16 | — | — | — | — |
| Q4_K_M | — | — | — | — |
| Q2_K | — | — | — | — |

**Success Criteria:** You can recommend a quantization level for: (a) production, (b) development, (c) edge devices.

---

### Exercise 10: Cost-Aware Agent (35 min)

**Task:** Build an agent that tracks and optimizes its own costs.

Implement a simple research agent that:
1. Breaks a query into sub-tasks
2. Estimates cost for each sub-task
3. Routes simple sub-tasks to SLM, complex to cloud
4. Reports total cost after execution

Test with: "Research and compare the top 3 vector databases for production RAG."

**Success Criteria:** Agent completes the task for <$0.10 and reports cost breakdown by sub-task.

---

## Portfolio Deliverables

After completing these exercises, add to your portfolio:

1. **Synthetic Dataset**: Your golden dataset with validation results
2. **Cost Comparison Report**: Model routing strategy with cost/accuracy trade-offs
3. **SLM Benchmark**: Local model performance comparison
4. **Hybrid Router**: Working prototype with cost savings demonstrated

---

## Interview Questions

1. When would you choose a reasoning model (o1/R1) over a standard LLM?
2. What are the key cost optimization strategies in a production AI system?
3. Compare RAG vs long-context approaches. When is each preferred?
4. How would you design a hybrid system using both local SLMs and cloud LLMs?
5. What is quantization and how does it affect deployment decisions?
6. How do you generate and validate synthetic data for RAG evaluation?
7. Describe the cost-accuracy-latency triangle and how you balance it.
8. What's the future of agentic workflows with SLMs?

---

## Common Mistakes

1. **Using reasoning models for everything** — 10x cost for no benefit on simple tasks
2. **Ignoring quantization impact** — Q2 can lose significant accuracy
3. **Not tracking costs** — You can't optimize what you don't measure
4. **Assuming local models are useless** — SLMs handle 60-80% of queries well
5. **Over-engineering the router** — Start simple (length-based), iterate
6. **No fallback strategy** — Always have a backup model if primary fails
7. **Not testing with real traffic patterns** — Benchmarks ≠ production

---

## Quick Reference

```bash
# Ollama commands
ollama pull llama3.2:3b
ollama list
ollama run llama3.2:3b
ollama stop llama3.2:3b

# OpenAI cost rates (2026)
gpt-4o-mini:    $0.15/1M input,   $0.60/1M output
gpt-4o:         $2.50/1M input,  $10.00/1M output
o3-mini:        $1.10/1M input,   $4.40/1M output
text-embedding: $0.02/1M tokens
whisper:        $0.006/minute