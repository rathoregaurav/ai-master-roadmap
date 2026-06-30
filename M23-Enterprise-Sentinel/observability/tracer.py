"""
Observability — Enterprise Sentinel Monitoring
================================================
OpenTelemetry tracing, cost tracking, and metrics collection.
"""

import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1. Span & Trace Models
# ──────────────────────────────────────────────

@dataclass
class Span:
    """A single span in a distributed trace."""
    id: str
    trace_id: str
    parent_id: Optional[str]
    name: str
    service: str
    start_time: float
    end_time: Optional[float] = None
    attributes: dict[str, Any] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)
    status: str = "ok"  # ok, error


@dataclass
class Trace:
    """A complete distributed trace."""
    id: str
    spans: list[Span] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None


# ──────────────────────────────────────────────
# 2. Tracer
# ──────────────────────────────────────────────

class Tracer:
    """
    Simple OpenTelemetry-compatible tracer.
    
    Tracks spans across services for distributed tracing.
    """

    def __init__(self, service_name: str = "enterprise-sentinel"):
        self.service_name = service_name
        self.traces: dict[str, Trace] = {}

    def start_trace(self) -> str:
        """Start a new trace."""
        trace_id = str(uuid.uuid4())
        self.traces[trace_id] = Trace(id=trace_id)
        logger.debug(f"Started trace: {trace_id}")
        return trace_id

    def start_span(
        self,
        name: str,
        trace_id: str,
        parent_id: Optional[str] = None,
        attributes: dict = None,
    ) -> Span:
        """Start a new span within a trace."""
        span = Span(
            id=str(uuid.uuid4()),
            trace_id=trace_id,
            parent_id=parent_id,
            name=name,
            service=self.service_name,
            start_time=time.time(),
            attributes=attributes or {},
        )

        if trace_id in self.traces:
            self.traces[trace_id].spans.append(span)

        logger.debug(f"Started span: {span.id} ({name}) in trace {trace_id}")
        return span

    def end_span(self, span: Span, status: str = "ok"):
        """End a span."""
        span.end_time = time.time()
        span.status = status

        # Update trace end time
        trace = self.traces.get(span.trace_id)
        if trace:
            trace.end_time = time.time()

    def add_event(self, span: Span, name: str, attributes: dict = None):
        """Add an event to a span."""
        span.events.append({
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {},
        })

    def get_trace_duration(self, trace_id: str) -> float:
        """Get the total duration of a trace in seconds."""
        trace = self.traces.get(trace_id)
        if not trace or not trace.end_time:
            return 0.0
        return trace.end_time - trace.start_time

    def get_trace_summary(self, trace_id: str) -> dict:
        """Get a summary of a trace."""
        trace = self.traces.get(trace_id)
        if not trace:
            return {"error": "Trace not found"}

        spans_by_service = {}
        for span in trace.spans:
            svc = span.service
            if svc not in spans_by_service:
                spans_by_service[svc] = []
            spans_by_service[svc].append({
                "name": span.name,
                "duration_ms": round((span.end_time - span.start_time) * 1000) if span.end_time else 0,
                "status": span.status,
            })

        return {
            "trace_id": trace_id,
            "total_spans": len(trace.spans),
            "services_involved": list(spans_by_service.keys()),
            "total_duration_ms": round(self.get_trace_duration(trace_id) * 1000),
            "spans_by_service": spans_by_service,
        }


# ──────────────────────────────────────────────
# 3. Cost Tracker
# ──────────────────────────────────────────────

@dataclass
class CostEntry:
    """A single cost tracking entry."""
    id: str
    service: str
    model: str
    input_tokens: int
    output_tokens: int
    estimated_cost: float
    latency_ms: float
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    trace_id: Optional[str] = None


class CostTracker:
    """Track costs across all services."""

    RATES = {
        "gpt-4o": {"input": 0.0025 / 1000, "output": 0.01 / 1000},
        "gpt-4o-mini": {"input": 0.00015 / 1000, "output": 0.0006 / 1000},
        "o3-mini": {"input": 0.0011 / 1000, "output": 0.0044 / 1000},
        "whisper-1": {"input": 0.006 / 60, "output": 0},  # $0.006/min
        "text-embedding-3-small": {"input": 0.00002 / 1000, "output": 0},
        "gpt-4o-vision": {"input": 0.005 / 1000, "output": 0.015 / 1000},
    }

    def __init__(self):
        self.entries: list[CostEntry] = []

    def track(
        self,
        service: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        trace_id: Optional[str] = None,
    ) -> CostEntry:
        """Record a cost entry."""
        rates = self.RATES.get(model, {"input": 0, "output": 0})
        cost = (input_tokens * rates["input"]) + (output_tokens * rates["output"])

        entry = CostEntry(
            id=str(uuid.uuid4()),
            service=service,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            estimated_cost=round(cost, 6),
            latency_ms=round(latency_ms, 1),
            trace_id=trace_id,
        )
        self.entries.append(entry)
        return entry

    def total_cost(self) -> float:
        return sum(e.estimated_cost for e in self.entries)

    def cost_by_service(self) -> dict[str, float]:
        costs = {}
        for e in self.entries:
            costs[e.service] = costs.get(e.service, 0) + e.estimated_cost
        return costs

    def cost_by_model(self) -> dict[str, float]:
        costs = {}
        for e in self.entries:
            costs[e.model] = costs.get(e.model, 0) + e.estimated_cost
        return costs

    def get_summary(self) -> dict:
        """Get a full cost summary."""
        return {
            "total_queries": len(self.entries),
            "total_cost": round(self.total_cost(), 6),
            "by_service": self.cost_by_service(),
            "by_model": self.cost_by_model(),
            "avg_cost_per_query": round(
                self.total_cost() / max(len(self.entries), 1), 8
            ),
            "avg_latency_ms": round(
                sum(e.latency_ms for e in self.entries) / max(len(self.entries), 1), 1
            ),
        }


# ──────────────────────────────────────────────
# 4. Metrics Collector
# ──────────────────────────────────────────────

class MetricsCollector:
    """
    Collect and expose Prometheus-compatible metrics.
    
    In production, this would use the `prometheus_client` library.
    """

    def __init__(self):
        self.metrics: dict[str, list[float]] = {
            "request_duration_ms": [],
            "request_tokens": [],
            "request_cost": [],
            "guardrail_blocks": [],
            "worker_latency_ms": [],
            "rag_relevance_score": [],
        }

    def record(self, metric_name: str, value: float):
        """Record a metric value."""
        if metric_name in self.metrics:
            self.metrics[metric_name].append(value)
            # Keep only last 1000 values
            if len(self.metrics[metric_name]) > 1000:
                self.metrics[metric_name] = self.metrics[metric_name][-1000:]

    def get_stats(self, metric_name: str) -> dict:
        """Get statistics for a metric."""
        values = self.metrics.get(metric_name, [])
        if not values:
            return {"min": 0, "max": 0, "avg": 0, "p50": 0, "p95": 0, "p99": 0, "count": 0}

        sorted_vals = sorted(values)
        n = len(sorted_vals)
        return {
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "avg": round(sum(values) / n, 2),
            "p50": round(sorted_vals[int(n * 0.5)], 2),
            "p95": round(sorted_vals[int(n * 0.95)], 2),
            "p99": round(sorted_vals[int(n * 0.99)], 2),
            "count": n,
        }

    def all_stats(self) -> dict:
        """Get statistics for all metrics."""
        return {name: self.get_stats(name) for name in self.metrics}

    def get_prometheus_text(self) -> str:
        """Generate Prometheus-compatible text format."""
        lines = []
        for name, values in self.metrics.items():
            if values:
                lines.append(f"# HELP sentinel_{name} {name} metric")
                lines.append(f"# TYPE sentinel_{name} gauge")
                for v in values[-10:]:  # Last 10 values
                    lines.append(f'sentinel_{name}{{source="enterprise-sentinel"}} {v}')
        return "\n".join(lines)


# ──────────────────────────────────────────────
# 5. Demo
# ──────────────────────────────────────────────

def demo():
    """Demonstrate observability in action."""
    tracer = Tracer(service_name="enterprise-sentinel-demo")
    cost_tracker = CostTracker()
    metrics = MetricsCollector()

    print("\n" + "="*60)
    print("Enterprise Sentinel - Observability Demo")
    print("="*60)

    # Simulate a request flow
    trace_id = tracer.start_trace()
    
    # Span 1: Guardrails check
    guard_span = tracer.start_span("guardrails.check_input", trace_id)
    time.sleep(0.05)
    tracer.add_event(guard_span, "input_checked", {"risk_score": 0.02})
    tracer.end_span(guard_span)
    metrics.record("request_duration_ms", 50)

    # Span 2: Agent supervisor route
    route_span = tracer.start_span("supervisor.route_query", trace_id, parent_id=guard_span.id)
    time.sleep(0.1)
    tracer.end_span(route_span)
    metrics.record("request_duration_ms", 100)

    # Span 3: RAG worker
    rag_span = tracer.start_span("rag_worker.process", trace_id, parent_id=route_span.id)
    time.sleep(0.2)
    cost_tracker.track("rag-worker", "gpt-4o-mini", 500, 200, 200, trace_id)
    tracer.end_span(rag_span)
    metrics.record("worker_latency_ms", 200)

    tracer.traces[trace_id].end_time = time.time()

    # Print results
    print(f"\nTrace Summary:")
    summary = tracer.get_trace_summary(trace_id)
    print(f"  Trace ID: {summary['trace_id'][:8]}...")
    print(f"  Spans: {summary['total_spans']}")
    print(f"  Duration: {summary['total_duration_ms']}ms")
    print(f"  Services: {', '.join(summary['services_involved'])}")

    print(f"\nCost Summary:")
    cost_summary = cost_tracker.get_summary()
    print(f"  Total: ${cost_summary['total_cost']:.6f}")
    print(f"  By Service: {cost_summary['by_service']}")

    print(f"\nMetrics (P95):")
    stats = metrics.all_stats()
    for name, stat in stats.items():
        print(f"  {name}: p95={stat['p95']}ms, avg={stat['avg']}ms")


if __name__ == "__main__":
    demo()