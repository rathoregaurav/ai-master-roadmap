# AI System Design Interview Scenarios

> 15 high-signal system design questions with structured solutions. Each scenario maps to your Phase 1-5 learnings.

## How To Use This Guide

For each scenario:
1. Read the scenario and constraints
2. Try to design the system yourself (10 min)  
3. Compare with the solution
4. Practice the explanation out loud
5. Identify which Phase/module this tests

---

## Scenario 1: Enterprise RAG Chatbot

**The Problem:** A company wants to let employees ask questions over 50,000 internal documents (PDFs, DOCX, Confluence pages). Documents are updated weekly. Responses must cite sources. Sensitive documents should be visible only to authorized roles.

**Constraints:**
- 500+ concurrent users
- Answers in < 5 seconds
- Must handle proprietary data never sent to public model APIs
- Audit trail for compliance

### Solution Sketch

```
┌─────────┐    ┌──────────┐    ┌────────────┐    ┌───────────┐
│  User   │───▶│  Auth N  │───▶│  Router    │───▶│  RAG      │
│  Chat   │    │  Gateway │    │  + Guard   │    │  Service  │
└─────────┘    └──────────┘    └────────────┘    └───────────┘
                                                    │
                                            ┌───────▼──────┐
                                            │  Retriever   │
                                            │  Hybrid      │
                                            └───────┬──────┘
                                                    │
                                            ┌───────▼──────┐
                                            │  Vector DB   │
                                            │  (pgvector)  │
                                            └──────────────┘
```

**Key Design Decisions:**

| Decision | Option | Why |
|----------|--------|-----|
| Embedding Provider | Open-source (BGE-M3) | Proprietary data never leaves |
| Vector DB | pgvector on RDS | Single DB, auth via row-level security |
| Chunking | Recursive + Semantic | PDFs need structure-aware splitting |
| Search | Hybrid (Vector + BM25) | Keywords matter for compliance docs |
| Caching | Redis semantic cache | Repeated queries are fast & cheap |
| Auth | JWT → Role-based → RLS | Tenant isolation at DB level |

**Interview Explanation (90-second version):**

> "For enterprise RAG, the primary constraint is data security. I choose pgvector over Pinecone because I need row-level security for document permissions. Hybrid search ensures both semantic matches and exact keyword matches. I batch ingestion as async jobs through SQS, and use semantic caching to handle repeated queries. The evaluation layer runs a golden dataset nightly to detect retrieval regressions."

**What This Tests:** Phase 2 (RAG), Phase 4 (Security, System Design), Phase 5 (AWS, Enterprise)

---

## Scenario 2: Multi-Agent Customer Support System

**The Problem:** An e-commerce company wants an AI agent that can handle refunds, order tracking, product questions, and returns. The agent must use internal APIs (orders, inventory, CRM) and escalate to humans for refunds over $500.

**Constraints:**
- Must handle 10,000 conversations/day
- Agents must never perform destructive actions without approval
- Each conversation must be recoverable if the system crashes
- Agents should learn from past successful resolutions

### Solution Sketch

```
┌──────────┐    ┌──────────────┐    ┌──────────────────┐
│  User    │───▶│  Supervisor  │───▶│  Classifier      │
│  Input   │    │  Agent       │    │  (Intent +       │
└──────────┘    └──────────────┘    │   Sentiment)     │
                                    └────────┬─────────┘
                                             │
                ┌────────────────────────────┼────────────────────┐
                ▼                            ▼                    ▼
        ┌──────────────┐            ┌──────────────┐    ┌──────────────┐
        │ Order Agent  │            │ Return Agent │    │ Product      │
        │ (Read tools) │            │ (Write tools)│    │ Agent        │
        └──────┬───────┘            └──────┬───────┘    └──────┬───────┘
               │                           │                   │
        ┌──────▼──────┐            ┌──────▼──────┐     ┌──────▼──────┐
        │ Order API   │            │ Return API  │     │ Search API  │
        │ Inventory   │            │ + Human     │     │ Reviews     │
        │ Tracking    │            │   Approval  │     │ FAQ         │
        └─────────────┘            └─────────────┘     └─────────────┘
```

**Key Design Decisions:**

| Decision | Option | Why |
|----------|--------|-----|
| Agent Framework | LangGraph with state | Checkpoints for crash recovery |
| Tool Permissions | Read-only vs Write-gated | Refunds > $500 need human approval |
| Memory | Episodic (conversation history) | Context across multi-turn |
| Evaluation | Task success rate + CSAT | Measure both accuracy and satisfaction |
| Fallback | Human handoff with full trace | If agent confidence < 0.7 |

**Interview Explanation (90-second version):**

> "For multi-agent support, the supervisor pattern is essential. The supervisor classifies intent and routes to specialized agents. Write operations (refunds, cancellations) go through a human approval gate. LangGraph gives me checkpoints so conversations survive crashes. I measure task success rate against a golden dataset, and route low-confidence cases to humans. The memory system stores resolved patterns so the agent improves over time."

**What This Tests:** Phase 3 (Agents, Tools, MCP), Phase 4 (Security), Phase 2 (Memory)

---

## Scenario 3: Cost-Optimized Multi-Model Gateway

**The Problem:** A startup uses OpenAI for production but wants to reduce costs by 60% without sacrificing quality. They have diverse traffic: simple chat, complex reasoning, RAG queries, and coding tasks.

**Constraints:**
- Must maintain response quality within 5% of GPT-4 baseline
- P95 latency < 3 seconds
- Must handle provider outages gracefully
- Different customers have different latency SLAs

### Solution Sketch

```
┌──────────┐    ┌──────────────┐    ┌──────────────────┐
│ Request  │───▶│  Classifier  │───▶│  Model Router    │
│          │    │  (task type, │    │  (cost + latency  │
│          │    │   SLA tier)  │    │   optimizer)      │
└──────────┘    └──────────────┘    └────────┬─────────┘
                                             │
                    ┌────────────────────────┼────────────────────┐
                    ▼                        ▼                    ▼
            ┌──────────────┐        ┌──────────────┐    ┌──────────────┐
            │ GPT-4o-mini  │        │ GPT-4o       │    │ Claude 3.5   │
            │ (Simple Q&A) │        │ (Reasoning)  │    │ (Coding)     │
            │ $0.15/Mtok   │        │ $2.50/Mtok   │    │ $3.00/Mtok   │
            └──────┬───────┘        └──────┬───────┘    └──────┬───────┘
                   │                       │                   │
            ┌──────▼──────┐        ┌──────▼──────┐    ┌──────▼──────┐
            │ Semantic    │        │ Semantic    │    │ Semantic    │
            │ Cache       │        │ Cache       │    │ Cache       │
            └─────────────┘        └─────────────┘    └─────────────┘
```

**Key Design Decisions:**

| Decision | Option | Why |
|----------|--------|-----|
| Router | Classifier → Cost-aware | Route simple queries to cheap models |
| Cache | Semantic (cosine > 0.92) | Identical intent, different wording |
| Fallback | Circuit breaker + retry | Provider outage → next best model |
| Monitoring | Token cost per route + latency | Optimize routing thresholds weekly |
| Compression | Prompt compression for long ctx | Reduce token usage 40% on complex queries |

**Interview Explanation (90-second version):**

> "The key insight is that not all queries need GPT-4. A lightweight classifier routes queries by task type and required quality. Simple Q&A goes to GPT-4o-mini, reasoning to GPT-4o, coding to Claude. Semantic caching catches repeated patterns. Circuit breakers handle provider failures with automatic fallback. I track cost per route and adjust thresholds weekly. This can save 60-70% while keeping quality within 5% of GPT-4 baseline."

**What This Tests:** Phase 4 (Cost Optimization), Phase 4 (System Design), Phase 3 (Routing)

---

## Scenario 4: Real-Time Document Processing Pipeline

**The Problem:** A healthcare company receives 10,000+ PDF documents daily (lab reports, clinical notes, insurance forms). These need to be processed, de-identified (PII removed), chunked, embedded, and stored for search.

**Constraints:**
- HIPAA compliance - zero PHI exposure to external APIs
- Processing must complete within 1 hour of upload
- Documents vary in structure (tables, scanned images, handwritten notes)
- Audit trail for every transformation step

### Solution Sketch

```
┌──────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────┐
│ Upload   │───▶│ S3 Bucket    │───▶│ SQS Queue       │───▶│ Lambda   │
│ (Signed  │    │ (Raw docs)   │    │ (Async trigger)  │    │ Worker   │
│  URL)    │    └──────────────┘    └──────────────────┘    └────┬─────┘
└──────────┘                                                      │
                                                          ┌──────▼─────┐
                                                          │ OCR        │
                                                          │ (Tesseract)│
                                                          │ + Layout   │
                                                          │ Detection  │
                                                          └──────┬─────┘
                                                                 │
                                                          ┌──────▼─────┐
                                                          │ De-identify│
                                                          │ (Regex +   │
                                                          │  NLP)      │
                                                          └──────┬─────┘
                                                                 │
                                                          ┌──────▼─────┐
                                                          │ Chunk +    │
                                                          │ Embed      │
                                                          │ (BGE-M3    │
                                                          │  local)    │
                                                          └──────┬─────┘
                                                                 │
                                                          ┌──────▼─────┐
                                                          │ pgvector   │
                                                          │ + Audit    │
                                                          │ Log        │
                                                          └────────────┘
```

**Key Design Decisions:**

| Decision | Option | Why |
|----------|--------|-----|
| OCR | Tesseract + LayoutLM | Handles tables and handwriting |
| PHI Removal | Regex + spaCy NER + human review sample | Multiple layers for HIPAA |
| Chunking | Structure-aware (by section) | Medical docs need semantic units |
| Processing | Async via SQS | Decouple upload from processing |
| Embedding | BGE-M3 (local) | Zero external API calls for PHI |

**Interview Explanation:**

> "Healthcare documents require a careful async pipeline. Upload goes to S3, which triggers an SQS message. Lambda workers pick up messages, run OCR for scanned documents, apply de-identification with regex and NER, then structure-aware chunking by medical section. Embedding happens locally with BGE-M3 so no PHI ever leaves our VPC. Every step logs document ID, timestamp, operation, and checksum for audit."

**What This Tests:** Phase 2 (Document Processing), Phase 5 (AWS), Phase 4 (Security), Phase 4 (System Design)

---

## Scenario 5: Real-Time AI Monitoring and Alerting System

**The Problem:** An AI platform runs 50+ RAG and agent deployments. The team needs to detect quality degradation, cost anomalies, security incidents, and latency spikes in real-time.

**Constraints:**
- Alert on any metric within 1 minute of anomaly
- Store 90 days of trace data
- Must distinguish between normal traffic spikes and actual degradation
- Compliance requires quarterly audit reports

### Solution Sketch

```
┌──────────┐    ┌──────────────┐    ┌──────────────────┐
│ Request  │───▶│ OpenTelemetry│───▶│ Metrics Pipeline │
│          │    │ Collector    │    │ (Prometheus)     │
└──────────┘    └──────────────┘    └────────┬─────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  Alert Manager  │
                                    │  (Rules Engine) │
                                    └────────┬────────┘
                                             │
                    ┌────────────────────────┼────────────────────┐
                    ▼                        ▼                    ▼
            ┌──────────────┐        ┌──────────────┐    ┌──────────────┐
            │ Telemetry    │        │ Dashboard    │    │ Incident     │
            │ (Traces +    │        │ (Grafana)    │    │ Manager      │
            │  Logs)       │        │              │    │ (PagerDuty)  │
            └──────────────┘        └──────────────┘    └──────────────┘
```

**Metrics to Track Per Request:**

| Category | Metrics | Anomaly Threshold |
|----------|---------|-------------------|
| Latency | P50, P95, P99, TTFT | P95 > 3s for 5 consecutive minutes |
| Quality | Groundedness score, User feedback (thumbs) | Score < 0.8 for 10+ requests |
| Cost | Tokens per request, Cost per user | Spike > 2x weekly average |
| Security | Injection attempts, PII detected | Any detection = P1 alert |
| System | Error rate, CPU, Memory | Error rate > 1% for 1 minute |

**Interview Explanation:**

> "I use OpenTelemetry to instrument every AI request with trace context. Each span captures: latency, model used, tokens, cost, retrieval scores, and evaluation metrics. Metrics go to Prometheus; traces to a telemetry store. AlertManager evaluates rules like 'P95 latency > 3s for 5 minutes' and pages the on-call engineer. The dashboard shows real-time and historical trends. For security, any injection detection is an instant P1. Quarterly, I generate compliance reports from stored traces."

**What This Tests:** Phase 4 (Observability), Phase 5 (Enterprise), Phase 4 (Cost)

---

## Scenario 6: Multi-Tenant AI Platform

**The Problem:** A company wants to offer AI assistant capabilities to 1,000+ different businesses. Each tenant has their own documents, custom prompts, team members, and billing.

**Constraints:**
- Zero data leakage between tenants
- Each tenant can customize their AI's behavior
- Usage-based billing per tenant
- Different tenants may need different model providers

### Solution Sketch

```
┌──────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────┐
│ Tenant A │───▶│ API Gateway  │───▶│ Multi-Tenant     │───▶│ Tenant   │
│ Users    │    │ (Auth +      │    │ Router           │    │ Context  │
└──────────┘    │  Rate Limit) │    │ (Tenant ID in    │    │ Store    │
                └──────────────┘    │  every request)  │    │ (Redis)  │
                                    └────────┬─────────┘    └──────────┘
                                             │
                    ┌────────────────────────┼────────────────────┐
                    ▼                        ▼                    ▼
            ┌──────────────┐        ┌──────────────┐    ┌──────────────┐
            │ RAG Engine   │        │ Agent Engine │    │ Custom       │
            │ (Tenant docs)│        │ (Tenant      │    │ Prompt       │
            │              │        │  tools)      │    │ Registry     │
            └──────┬───────┘        └──────┬───────┘    └──────┬───────┘
                   │                       │                   │
            ┌──────▼──────┐        ┌──────▼──────┐    ┌──────▼──────┐
            │ Vector DB   │        │ Tool Store  │    │ Tenant      │
            │ (RLS per    │        │ (per tenant)│    │ Config      │
            │  tenant)    │        │             │    │ (DB)        │
            └─────────────┘        └─────────────┘    └─────────────┘
```

**Key Design Decisions:**

| Decision | Option | Why |
|----------|--------|-----|
| Tenant Isolation | Row-level security in DB | Data never mixes at storage level |
| Auth | JWT with tenant_id claim | Every request is scoped |
| Customization | Per-tenant prompt + model config | Stored in tenant config table |
| Billing | Usage-aggregated per tenant_id | Track tokens, API calls, storage |
| Rate Limiting | Tiered (per tenant SLA) | Gold vs Silver vs Free tenants |

**Interview Explanation:**

> "Multi-tenancy requires isolation at every layer. Auth embeds tenant_id in JWT claims. The database uses row-level security so queries naturally scope to one tenant. Each tenant has their own prompt registry entries, tool configurations, and document collections. I aggregate billing by tenant_id across all services. Rate limiting is tiered per tenant SLA. The key principle: tenant_id is threaded through every request, service call, and data query so isolation is automatic."

**What This Tests:** Phase 5 (Enterprise, Multi-Tenancy), Phase 4 (Security, System Design)

---

## Scenario 7: Fine-Tuning vs RAG Decision System

**The Problem:** A company needs to help customers decide whether to fine-tune or use RAG for their specific use case. Build a decision framework.

### Decision Framework

```
┌─────────────────────────────┐
│  Knowledge Type?            │
│  - Static/stable → FT       │
│  - Dynamic/changing → RAG   │
│  - Both → Hybrid            │
└─────────────┬───────────────┘
              │
    ┌─────────▼─────────┐
    │  Data Volume?     │
    │  < 1000 docs → RAG│
    │  > 100K docs → FT │
    │  In between → Eval│
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  Latency SLA?     │
    │  < 500ms → FT     │
    │  > 2s → RAG fine  │
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  Auditability?    │
    │  Required → RAG   │
    │  Not needed → FT  │
    └───────────────────┘
```

**Interview Explanation:**

> "The RAG vs Fine-tuning decision depends on four factors. RAG wins when knowledge changes frequently, when you need source citations for compliance, and when volume is moderate. Fine-tuning wins when you need consistent format, very low latency, and the knowledge is static. In practice, many production systems use a hybrid: fine-tune for behavior/tone, RAG for knowledge."

---

## Scenario 8: AI Agent with Memory and Personalization

**The Problem:** A personal AI assistant that learns user preferences over time, remembers past conversations, and adapts to each user's communication style.

**Constraints:**
- Must work across sessions (days/weeks apart)
- Must forget when asked (GDPR compliance)
- Should improve with each interaction
- Must handle 1M+ users

### Memory Architecture

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ User Message │───▶│ Working Memory    │───▶│ Episodic Memory  │
│              │    │ (Session context) │    │ (Past sessions)  │
└──────────────┘    └──────────────────┘    └────────┬─────────┘
                                                      │
                                             ┌────────▼─────────┐
                                             │ Semantic Memory  │
                                             │ (User facts:     │
                                             │  preferences,    │
                                             │  style, domain)  │
                                             └────────┬─────────┘
                                                      │
                                             ┌────────▼─────────┐
                                             │ Consolidation    │
                                             │ (Evening batch   │
                                             │  - compress +    │
                                             │   evict stale)   │
                                             └──────────────────┘
```

**Key Design Decisions:**

| Decision | Option | Why |
|----------|--------|-----|
| Working Memory | In-context (session) | Automatic, no storage needed |
| Episodic | Embedding store + time-decay | Recent conversations matter more |
| Semantic | Structured KV store | Explicit user facts |
| Eviction | LRU + relevance score + age | Don't grow unbounded |
| Deletion | Tombstone + re-index | GDPR right to be forgotten |

**Interview Explanation:**

> "Three-tier memory: working memory for the current session, episodic memory for past conversations stored as embeddings with time-decay, and semantic memory for extracted user facts in a structured store. A nightly consolidation job compresses, deduplicates, and evicts stale memories. For GDPR, deletion writes tombstones that exclude those embeddings from retrieval. The system improves over time as it accumulates more user signals."

---

## Fast Interview Drills (15 Scenarios, 2 Minutes Each)

1. **Design a system that summarizes 1,000 pages/hour** → Async batch, map-reduce summarization, cost optimization
2. **Design a system that detects prompt injection in real-time** → Input guardrail, classifier, rate limiting, audit log
3. **Design an A/B testing framework for prompts** → Feature flags, prompt registry versioning, evaluation metrics
4. **Design a system that routes customer emails to the right department** → Classifier agent, tool calling, fallback to human
5. **Design a RAG system that handles tables** → Table-aware chunking, HTML parser, structured retrieval
6. **Design a caching strategy for a multi-model AI app** → Exact cache, semantic cache, TTL, invalidation
7. **Design a system to measure AI answer quality without humans** → LLM-as-a-judge, golden dataset, groundedness scoring
8. **Design a system that generates synthetic data for testing** → Prompt chaining, quality filters, diversity sampling
9. **Design a system for secure multi-agent communication** → MCP with auth, scoped tool permissions, audit trail
10. **Design a cost-tracking system for AI usage** → Token counting per model, per user, per feature, budget alerts
11. **Design a system that handles model provider migration** → API abstraction layer, canary testing, traffic shifting
12. **Design an AI-powered search for an internal wiki** → Hybrid search, reranking, snippet generation, feedback loop
13. **Design a system for monitoring hallucinations** → LLM-as-a-judge, consistency checks, citation verification
14. **Design a system for AI-powered code review** → Code RAG, diff analysis, review agent, CI integration
15. **Design a system for real-time document collaboration** → WebSocket streaming, CRDT, AI suggestions, conflict resolution

---

## Study Plan

| Week | Focus | Scenarios |
|------|-------|-----------|
| 1 | RAG Architecture | 1, 4, 12 |
| 2 | Agent Systems | 2, 8, 14 |
| 3 | Production AI | 3, 5, 10 |
| 4 | Enterprise & Scale | 6, 7, 9, 11 |
| 5 | Fast Drills | All 15 drills |
| 6 | Mock Interviews | Any 3 scenarios, timed |