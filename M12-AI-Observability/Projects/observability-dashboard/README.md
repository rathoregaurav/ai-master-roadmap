# Observability Dashboard - M12 Project

> Real-time monitoring dashboard for AI system metrics: latency, tokens, cost, and quality scores.

## Architecture

```
AI Request → OpenTelemetry → Metrics (Prometheus) → Dashboard (Grafana)
                              Traces (Jaeger)
                              Logs (Structured)
```

## Metrics to Track

```python
# metrics.py
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class AIRequestMetrics:
    request_id: str
    user_id: str
    model: str
    tokens_input: int
    tokens_output: int
    latency_ms: float
    cost: float
    groundedness_score: float = 0.0
    user_feedback: int = 0  # -1, 0, 1
    error: str = ""
    timestamp: str = ""
    
    def to_dict(self):
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "model": self.model,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "total_tokens": self.tokens_input + self.tokens_output,
            "latency_ms": self.latency_ms,
            "cost": self.cost,
            "groundedness_score": self.groundedness_score,
            "user_feedback": self.user_feedback,
            "error": self.error,
            "timestamp": self.timestamp or datetime.now().isoformat()
        }

class MetricsStore:
    def __init__(self):
        self._metrics = []
    
    def record(self, metric: AIRequestMetrics):
        self._metrics.append(metric)
    
    def summary(self) -> dict:
        if not self._metrics:
            return {}
        latencies = [m.latency_ms for m in self._metrics]
        costs = [m.cost for m in self._metrics]
        
        return {
            "total_requests": len(self._metrics),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)],
            "total_cost": sum(costs),
            "avg_cost_per_request": sum(costs) / len(costs),
            "error_rate": sum(1 for m in self._metrics if m.error) / len(self._metrics),
            "avg_groundedness": sum(m.groundedness_score for m in self._metrics) / len(self._metrics)
        }
```

## Project Structure

```
observability-dashboard/
├── metrics.py             # Metrics collection and storage
├── tracing.py             # OpenTelemetry trace setup
├── dashboard.py           # Dashboard API (FastAPI)
├── alerts.py              # Alerting rules engine
├── templates/             # Dashboard HTML templates
├── requirements.txt
└── README.md