# Load-Tested RAG - M18 Project

> A RAG system with load testing, benchmarking, and performance optimization.

## Architecture

```
Load Generator (Locust) → RAG API → (Retriever → LLM → Response) → Metrics Collection
```

## Load Test Plan

```python
# locustfile.py
from locust import HttpUser, task, between
import random

class RAGUser(HttpUser):
    wait_time = between(1, 5)  # Simulate user think time
    
    @task(3)
    def ask_simple_question(self):
        self.client.post("/ask", json={
            "query": "What is the refund policy?",
            "user_id": f"load_test_user_{random.randint(1, 100)}"
        })
    
    @task(2)
    def ask_complex_question(self):
        self.client.post("/ask", json={
            "query": "Compare the refund policies for electronics and clothing, and explain the exceptions",
            "user_id": f"load_test_user_{random.randint(1, 100)}"
        })
    
    @task(1)
    def search_documents(self):
        self.client.post("/search", json={
            "query": "shipping",
            "top_k": 5
        })

# Run: locust -f locustfile.py --host=http://localhost:8000
```

## Benchmark Results Template

```
Load Test Results
=================
Date: 2026-07-01
Scenario: 50 concurrent users, ramp over 5 min, sustain 10 min

Latency:
  P50:   1.2s
  P95:   3.8s  
  P99:   6.1s
  TTFT:  0.4s (P50)

Throughput:
  Requests/sec: 45
  Total requests: 27,000

Errors:
  Rate: 0.3%
  Timeouts: 12
  5xx: 2

Cost:
  Avg cost/request: $0.0042
  Total inference cost: $113.40

Recommendations:
  1. Add semantic caching (est. 40% latency reduction)
  2. Increase retriever pool size (current bottleneck at 50 concurrent)
  3. Consider GPT-4o-mini for simple queries
```

## Project Structure

```
load-tested-rag/
├── app/                    # RAG application
│   ├── main.py
│   ├── retriever.py
│   └── generator.py
├── tests/
│   ├── locustfile.py       # Load test scenarios
│   └── benchmark.py        # Benchmark runner
├── results/                # Test results
├── docker-compose.yml      # With Prometheus + Grafana
├── requirements.txt
└── README.md