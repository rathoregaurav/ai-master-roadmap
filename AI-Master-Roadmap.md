# AI-Master-Roadmap: Complete 36-Week Curriculum

## Guiding Principles

1. **Job market demand in 2026** (RAG and Agents are #1, Multimodal is #5)
2. **Dependency logic** (you can't do Agents without Tools, you can't do MCP without Agents)
3. **"Show-me-the-money" velocity** (getting you a deployable, evaluable prototype in the first 4 weeks)

---

## PHASE 1: The Launchpad (Weeks 1–3)

*Goal: Get a production-grade AI API deployed by Day 7.*

- **Week 1:** M0 (AI Engineering Foundations) + M3 (LLM Fundamentals)
  - Set up Docker/VS Code environment
  - Call OpenAI/Anthropic via `httpx`
  
- **Week 2:** M1 (Python for AI Engineering)
  - Focus: Pydantic v2, Async, and Loguru
  - Pair with M4 (Prompt Engineering)
  - Master: System Prompts, XML/JSON prompting, Structured Outputs
  
- **Week 3:** M2 (Backend Engineering for AI)
  - Build FastAPI app with Streaming SSE
  - Background Workers and JWT auth
  - Deploy on free tier

> **Milestone 1:** *AI Utility Toolkit (Live API with prompt playground & structured output)*

---

## PHASE 2: The RAG Fortress (Weeks 4–7)

*Goal: Master retrieval. You cannot be an AI Engineer without this.*

*Highest Industry Priority*

- **Week 4:** M5 (Embeddings) + M6 (RAG - Document Processing & Chunking)
  - Master semantic search
  - Cosine similarity
  - Recursive/semantic chunking for PDFs and DOCXs
  
- **Week 5:** M6 (RAG - Retrieval & Vector DBs)
  - Hybrid search
  - Metadata filtering
  - Hands-on: Qdrant and pgvector
  
- **Week 6:** M6 (Advanced RAG)
  - Query rewriting
  - Multi-query
  - Reranking (Cohere)
  - Context Compression
  
- **Week 7:** M11 (AI Evaluation) — *Moved up!*
  - Build Golden Datasets
  - Calculate Recall/MRR
  - Implement LLM-as-a-Judge for RAG groundedness evaluation

> **Milestone 2:** *Enterprise RAG Platform (with an evaluation dashboard)*

---

## PHASE 3: The Agentic Stack (Weeks 8–13)

*Goal: Build systems that act, not just chat.*

*2026's Defining Trend*

- **Week 8:** M8 (Tool Calling)
  - Master JSON Schema
  - Parallel tool calls
  - Build API/SQL/Calendar tools with error recovery
  
- **Week 9:** M7 (AI Agents - Architecture & LangGraph)
  - State machines
  - ReAct agents
  - Supervisor pattern
  
- **Week 10:** M7 (Advanced Agents)
  - Reflection
  - Critique
  - Human-in-the-loop
  - Checkpoints
  - Build multi-worker research team
  
- **Week 11:** M9 (Model Context Protocol - MCP)
  - Moved up to reflect current hype & enterprise demand!
  - Build MCP Server that exposes internal tools/resources
  - Connect to any MCP Client
  
- **Week 12:** M10 (Memory Systems)
  - Semantic Memory
  - Episodic Memory
  - Knowledge Memory
  - Memory compression and eviction for long-running agents
  
- **Week 13:** Integration Week
  - Combine Agents + MCP + Memory into single workflow

> **Milestone 3:** *Agentic Operations Assistant (with MCP connectors)*

---

## PHASE 4: The "Senior Engineer" Differentiator (Weeks 14–18)

*Goal: Trust, Security, and Scale. This is what gets you the Staff title.*

- **Week 14:** M13 (AI Security)
  - Massive demand right now
  - Prompt injection defense
  - Jailbreak detection
  - PII scrubbing
  - Output guardrails
  
- **Week 15:** M12 (AI Observability)
  - OpenTelemetry traces
  - Track token/cost per request
  - Build monitoring dashboard (LangSmith/Arize)
  
- **Week 16:** M15 (AI System Design)
  - Caching (Redis)
  - Queues (SQS/RabbitMQ)
  - Circuit Breakers
  - Fallback model routing
  
- **Week 17:** M18 (Production Engineering)
  - GitHub Actions CI/CD
  - Load testing (Locust)
  - Benchmark RAG latency
  
- **Week 18:** M20 (Cost Optimization)
  - Semantic caching
  - Prompt compression
  - Intelligent model routing (gpt-3.5 vs gpt-4 vs local SLMs)

> **Milestone 4:** *Production-hardened RAG + Agent system with full observability and sub-200ms caching*

---

## PHASE 5: Infrastructure & Enterprise (Weeks 19–24)

*Goal: Deploy at scale and satisfy the compliance team.*

- **Week 19:** M16 (AWS for AI)
  - S3
  - Lambda (for async doc processing)
  - ECS
  - Secrets Manager
  
- **Week 20:** M17 (Kubernetes)
  - Deployments
  - Services
  - Ingress
  - GPU node scheduling for open-weight models
  
- **Week 21:** M19 (AI Product Engineering)
  - Build Chat UI with streaming
  - Feedback thumbs-up/down
  - A/B testing feature flags
  
- **Week 22:** M21 (Enterprise AI)
  - Prompt Registry
  - Model Registry
  - Audit Logs
  - Data Lineage
  
- **Weeks 23–24:** Buffer & Deep-Dive
  - Revisit weak spots from M1–M21
  - Solidify System Design interview skills

> **Milestone 5:** *Enterprise AI Platform (Auth, Audits, and Admin Panel)*

---

## PHASE 6: Future-Proofing & Trends (Weeks 25–30)

*Goal: Stay ahead of the curve. All the "nice-to-haves" live here.*

*Detailed guide → [`PHASE-6-FUTURE-PROOFING.md`](./PHASE-6-FUTURE-PROOFING.md)*

- **Week 25:** M14 (Multimodal AI)
  - Vision models (GPT-4o vision, Claude 3.5)
  - OCR for scanned PDFs
  - Text-to-Speech
  
- **Week 26:** M22 (Market Trends - Deep Dive Pt.1)
  - Reasoning Models (o1/o3, DeepSeek R1)
  - Long-context strategies
  - Synthetic Data Generation
  
- **Week 27:** M22 (Market Trends - Pt.2)
  - Small Language Models (SLMs) vs Edge AI
  - Open-weight ecosystem (Llama 4, Mistral)
  - Hybrid Agentic Workflows
  
- **Weeks 28–30:** Open-Source Contribution & Polish
  - Pick trending OSS project (LangGraph, DSPy, AutoGen)
  - Submit meaningful PR
  - Refine GitHub portfolio documentation

> **Milestone 6:** *Multi-Modal Research Assistant (accepts text, images, and audio)*

---

## PHASE 7: The Capstone Crucible (Weeks 31–36)

*Detailed guide → [`PHASE-7-CAPSTONE-CRUCIBLE.md`](./PHASE-7-CAPSTONE-CRUCIBLE.md)*

*Goal: Build your definitive portfolio piece that combines EVERYTHING.*

- **Weeks 31–36 (6 Weeks of Pure Building)**

Build **"Enterprise Sentinel"** – an end-to-end AI system that:

- Ingests multimodal data (PDFs, images, Slack transcripts) via MCP
- Routes queries via Agentic Supervisor to specialized RAG or SQL workers
- Includes Human-in-the-loop approval for destructive actions
- Has full OpenTelemetry observability, cost-tracking, and guardrail layer against prompt injection
- Deployed on Kubernetes with auto-scaling and A/B testable prompt variants
- Backed by Golden Dataset with 95%+ groundedness regression tests

> **Final Milestone 7:** *Complete Capstone Enterprise AI System (public GitHub repo with stellar README, architecture diagrams, and live demo link)*

---

## Summary of Changes (Priority Reordering)

| Original | New Priority | Reasoning |
|----------|--------------|-----------|
| M11 (Eval) @ Week ~30 | **Week 7** | You can't build RAG without testing it. Eval drives engineering. |
| M9 (MCP) @ Late | **Week 11** | MCP is hottest enterprise protocol in 2026; learn right after basic agents. |
| M13 (Security) @ Mid | **Week 14** | Security is now top-3 interview topic for Senior AI Engineers. |
| M14 (Multimodal) @ Mid | **Week 25** | <10% of enterprise jobs require video/audio today. Keep as secret weapon. |
| M22 (Trends) @ List | **Weeks 26–27** | Dedicated deep-dive instead of superficial overview. |

---

## PHASE 8: COMPLETE STAFF AI ADDENDUM

*Detailed guide → [`PHASE-8-STAFF-AI-ADDENDUM.md`](./PHASE-8-STAFF-AI-ADDENDUM.md)*

*Advanced Topics & Continuous Development*

### 1. Math Awareness (Conceptual Only)
- Vectors · Cosine Similarity · Matrix intuition
- Conditional Probability
- Precision/Recall/F1 · ROC/AUC

### 2. Data Engineering
- Batch/Streaming pipelines · ETL/ELT
- Document normalization (PDF/DOCX/HTML)
- OCR pipelines · Metadata enrichment
- Deduplication · CDC
- Incremental/Re-indexing

### 3. AI Testing
- Unit/Integration/Regression/Chaos tests
- Prompt regression · Golden datasets
- Synthetic data · Mock LLM testing
- Load/Chaos testing
- Evaluation-Driven Development

### 4. Enterprise Architecture (7 Layers)
- API Gateway · Inference · Prompt · Memory
- Vector · Database · Caching
- Event-driven (Queues/Workers)
- Microservices vs Monolith
- Multi-region/DR · Multi-tenancy
- Model/AI Gateway

### 5. Design Patterns (Complete Set)
- Workflow vs Agent
- Single/Multi/Hierarchical/Swarm
- Router · Reflection · Critic · Debate
- Planner-Executor
- Tree/Graph Search
- Dynamic Tool/Prompt Selection
- Retrieval Router
- Hybrid Workflow+Agent
- Human-in-the-Loop

### 6. Performance Engineering
- Latency profiling (P95/TTFT)
- Token/Prompt compression
- Semantic Caching
- Prompt/Embedding Cache
- Vector index tuning (HNSW/IVF_PQ)
- Batch/Continuous batching
- Cold starts

### 7. Open Source & Local Models
- Ollama/vLLM/TGI
- Quantization (GGUF/GPTQ/AWQ)
- Paged attention · GPU basics (VRAM/parallelism)
- CPU inference (SLMs)
- Open-weight models (Llama/Mistral/Qwen/DeepSeek)

### 8. Reasoning & Coding Agents
- Reasoning models (o1/R1)
- Thinking Budget & Effort
- Cost/Latency/Accuracy tradeoffs
- Code RAG (repo indexing)
- PR generation · Bug-fixing agents
- Review/CI-CD agents

### 9. Enterprise Integrations & Domains
- **Platforms:** Slack/Teams · GitHub/Jira/Confluence · Salesforce/CRM · Google/MS 365 · Webhooks/GraphQL
- **Domains:** Insurance (ACORD) · Finance · Healthcare (FHIR) · Legal · Retail · HR · Manufacturing

### 10. AI UX & Human-in-the-Loop
- Streaming UX · Interruptibility
- Progressive responses
- Chain-of-thought transparency
- Confidence display
- Citation hover/previews
- Human approval interfaces

### 11. Portfolio Productization (Per Project)
- Architecture diagram (C4)
- API docs (Swagger)
- Docker/Deploy guide
- Evaluation report · Benchmark results
- Security checklist · CI/CD pipeline
- Demo video · README with tradeoffs

### 12. The 4 Continuous Tracks (Run in Parallel)
- **A)** Portfolio polishing
- **B)** Interview prep (20 Qs/week)
- **C)** AI News (arXiv/HF, 30 min/week)
- **D)** Engineering Hygiene (Testing/Logging/Metrics/Security in every deliverable)

