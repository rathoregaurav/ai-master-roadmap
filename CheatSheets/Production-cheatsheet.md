# Production AI Engineering Cheat Sheet

> Quick reference for production AI engineering. Covers Phase 4.

## Latency Budget Template

```
Total Response Time Budget = 3-5 seconds
├── Auth + Routing: 100ms
├── Input Guardrail: 50ms  
├── Retrieval: 200ms
│   ├── Embed query: 50ms
│   ├── Vector search: 50ms
│   └── Reranking: 100ms
├── LLM Generation: 2-3s (streaming first token: 500ms)
├── Output Guardrail: 50ms
└── Response: Varies (streaming)
```

## Observability Stack

| Component | Tool | What It Tracks |
|-----------|------|----------------|
| Metrics | Prometheus | Latency (P50/P95/P99), error rate, request rate, cost |
| Traces | OpenTelemetry + Jaeger | Request flow through services |
| Logs | Structured (JSON) | Every LLM call, tool call, decision |
| Dashboard | Grafana | Visual metrics, trends, alerts |
| Alerting | AlertManager | Rule-based notifications |
| AI-specific | LangSmith / Arize | Traces, token usage, eval scores |

## AI-Specific Metrics

| Category | Metric | How to Measure |
|----------|--------|----------------|
| Latency | Time to First Token (TTFT) | Time from request to first output token |
| Latency | Total generation time | Time for complete response |
| Quality | Groundedness score | LLM-as-judge: does answer only use provided context? |
| Quality | User satisfaction | Thumbs up/down, rating 1-5 |
| Quality | Retrieval precision | % of retrieved chunks that were relevant |
| Cost | Tokens per request | Input + output tokens summed |
| Cost | Cost per request | Tokens × model rate |
| Cost | Cost per user | Aggregate per user_id |
| Reliability | Error rate | % of requests that failed |
| Reliability | Empty retrieval rate | % of queries with zero relevant results |

## CI/CD Pipeline for AI Systems

```
PR → Lint → Unit Tests → Eval Suite → Build → Staging → Canary → Production
```

### Pipeline Stages

1. **Lint**: Code style, type checking (mypy, ruff)
2. **Unit Tests**: Test individual components (mocked LLM responses)
3. **Eval Suite**: Run golden dataset, check metrics (Recall@K > 0.85, groundedness > 0.8)
4. **Build**: Docker build, push to registry
5. **Staging**: Deploy to staging, run integration tests + evals
6. **Canary**: 5% traffic → 25% → 100% (monitor metrics at each step)
7. **Production**: Full rollout, monitoring

### Rollback Triggers
- Error rate > 1%
- P95 latency > 3s
- Groundedness score drop > 5%
- User feedback score drop > 0.5
- Cost per request > 2x baseline

## Load Testing with Locust

```python
# Example Locust test for RAG API
class RAGUser(HttpUser):
    @task
    def ask_question(self):
        self.client.post("/ask", json={
            "query": "What is the refund policy?",
            "user_id": "test_123"
        })
```

### Load Test Plan

1. **Baseline**: 1 user, measure P50/P95 latency
2. **Ramp**: 1 → 50 users over 5 minutes
3. **Steady**: 50 concurrent users for 10 minutes
4. **Spike**: 50 → 200 users instantly
5. **Sustained**: 200 users for 5 minutes
6. **Cool down**: 200 → 0 over 2 minutes

### Metrics to Capture
- Requests per second
- P50/P95/P99 latency
- Error rate
- Memory usage per request
- CPU utilization
- LLM provider latency (not just total)

## Circuit Breaker Pattern

```
Closed → (errors > threshold) → Open → (cooldown period) → Half-Open → (try request) → Closed or Open again
```

### Configuration
- Error threshold: 50% errors in 1 minute
- Cooldown: 30 seconds
- Half-open max requests: 3
- Fallback: cache → fallback model → degraded response

## Cost Optimization Checklist

- [ ] Semantic caching implemented (30-50% cost reduction)
- [ ] Model routing: cheap model for simple queries
- [ ] Prompt compression for long contexts (40-60% token reduction)
- [ ] Embedding caching for frequent queries
- [ ] Batch processing for async tasks
- [ ] Token limits on output (max_tokens ceiling)
- [ ] Cost tracking per user, per feature, per model
- [ ] Budget alerts at 50%, 80%, 100%
- [ ] Regular audit of expensive model usage