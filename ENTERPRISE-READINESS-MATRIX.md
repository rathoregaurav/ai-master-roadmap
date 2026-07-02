# Enterprise Readiness Matrix

Use this file as the master audit checklist for the roadmap. A module is complete only when it supports learning, interviews, real work, and portfolio proof.

## Universal Module Standard

Every module should produce six artifacts:

| Artifact | What good looks like |
| --- | --- |
| Learning notes | You can explain the concept using the 7-question framework. |
| Working code | At least one example runs locally or has a clear dry-run path. |
| Interview proof | You can answer 3-5 common questions without reading notes. |
| System design proof | You can draw where the concept fits in an AI platform. |
| Production proof | You identify security, observability, cost, latency, and failure concerns. |
| Portfolio proof | The module improves a lab, project, or capstone artifact. |

## Module Outcomes

| Module | Learning outcome | Interview outcome | Real-work outcome | Enterprise check |
| --- | --- | --- | --- | --- |
| M0 Foundations | Reproducible workspace, secrets, Docker basics | Explain env isolation and secret handling | Start projects consistently | `.env.example`, pinned deps, README setup |
| M1 Python | Pydantic, async, logging, retries | Explain async and validation trade-offs | Build reliable service glue code | Typed boundaries, timeout policy |
| M2 Backend | FastAPI, streaming, auth, workers | Design an AI API | Ship API endpoints and background work | Auth, rate limits, health checks |
| M3 LLM Fundamentals | Tokens, context, sampling, API failure modes | Explain hallucination and structured output | Choose model settings safely | Model/version tracking |
| M4 Prompt Engineering | Prompt contracts, schemas, examples | Debug prompt failures | Build repeatable prompt workflows | Prompt versioning and regression tests |
| M5 Embeddings | Vector meaning and similarity | Compare lexical and semantic search | Build semantic search features | Benchmark model against real queries |
| M6 RAG | Ingestion, chunking, retrieval, reranking | Design enterprise RAG | Build grounded document QA | Citations, golden dataset, freshness |
| M7 Agents | State, tool use, supervisors, stopping rules | Compare workflow vs agent | Build controlled multi-step assistants | Max steps, checkpoints, audit logs |
| M8 Tool Calling | JSON schema, validation, tool execution | Explain tool safety | Connect LLMs to APIs and databases | Permissions and structured errors |
| M9 MCP | Standard tool/resource connector pattern | Explain MCP server/client roles | Expose internal tools consistently | Least privilege, audit, resource scopes |
| M10 Memory | Semantic, episodic, and knowledge memory | Explain memory risks | Add personalization and continuity | Retention, deletion, sensitivity policy |
| M11 Evaluation | Golden datasets, metrics, judges | Explain eval-driven development | Detect regressions before release | Versioned eval suites and thresholds |
| M12 Observability | Logs, metrics, traces, AI metadata | Debug a bad AI answer | Operate production systems | Request IDs, prompt/model/token/cost traces |
| M13 Security | Prompt injection, PII, tool abuse | Threat-model AI systems | Add guardrails and approval gates | Red-team cases, PII policy |
| M14 Multimodal | Vision, OCR, audio, multimodal RAG | Explain pipeline vs native models | Process screenshots, scans, audio | Data privacy and media retention |
| M15 System Design | Caches, queues, breakers, fallbacks | Solve AI system design rounds | Architect scalable AI platforms | SLOs, degradation, dependency map |
| M16 AWS | S3, Lambda, ECS, IAM, secrets | Explain cloud deployment choices | Deploy document workflows | IAM least privilege and cost tags |
| M17 Kubernetes | Deployments, services, ingress, autoscaling | Explain K8s primitives | Run AI services at scale | Probes, HPA, resource limits |
| M18 Production | CI/CD, load tests, rollout, readiness | Explain release safety | Ship and rollback safely | Production readiness checklist |
| M19 Product | Streaming UX, feedback, A/B testing | Explain AI product trade-offs | Build usable AI interfaces | Feedback loops and consent |
| M20 Cost | Caching, compression, routing | Optimize model spend | Reduce cost without quality loss | Budgets, alerts, per-tenant usage |
| M21 Enterprise AI | Governance, registry, audit, tenancy | Explain enterprise controls | Build admin and governance layers | Audit logs, lineage, RBAC |
| M22 Trends | Reasoning, long context, SLMs, synthetic data | Discuss current landscape clearly | Pick new tools responsibly | Benchmark before adoption |
| M23 Sentinel | Integrates all modules | Present capstone architecture | Build end-to-end enterprise system | Security, eval, observability, deployment |

## Enterprise Project Gate

Before calling any project enterprise-ready, confirm:

- Authentication and authorization are described.
- Data boundaries and tenant isolation are clear.
- Prompts, models, tools, and evals are versioned.
- Logs avoid secrets and raw sensitive data.
- Cost is measurable per request, feature, or tenant.
- Failure behavior is documented for model, vector DB, queue, and tool failures.
- Security tests include prompt injection, PII leakage, and unsafe tool calls.
- Observability includes request IDs, traces, latency, token counts, and model names.
- Deployment includes health checks, rollback, and environment variables.
- README includes architecture, setup, usage, trade-offs, and demo path.

## Interview Readiness Gate

For each phase, practice:

- One 60-second explanation per module.
- One system design question using that phase's milestone project.
- One debugging story: what failed, how you observed it, how you fixed it.
- One trade-off explanation: why this architecture instead of an alternative.

