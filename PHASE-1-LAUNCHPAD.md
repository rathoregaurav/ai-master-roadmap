# Phase 1: The Launchpad

Goal: build and deploy a useful AI API foundation in three weeks.

Phase 1 is where you stop being a passive learner and start behaving like an AI engineer. The focus is not only "call an LLM API"; the focus is learning how to package AI behavior inside clean Python, reliable APIs, typed schemas, streaming responses, logging, authentication, and deployable project structure.

For your AI transition, Phase 1 gives you the base engineering muscle. Every future RAG, agent, MCP, memory, and evaluation system will reuse these same fundamentals.

## Weekly Plan

| Week | Modules | Main outcome |
| --- | --- | --- |
| 1 | M0 + M3 | Local AI engineering environment and first typed LLM API calls |
| 2 | M1 + M4 | Python patterns for AI apps and prompt/structured-output workflows |
| 3 | M2 | FastAPI AI Utility Toolkit with streaming and background jobs |

## Phase Deliverable

Build the `AI Utility Toolkit`: a FastAPI service that exposes:

- `/health` for uptime checks
- `/prompt/structured` for validated JSON responses
- `/prompt/stream` for Server-Sent Events streaming
- `/jobs` for background tasks
- `/auth/token` for JWT-style auth practice

Starter project: `M2-Backend-Engineering-for-AI/Projects/ai-utility-toolkit/`

## End-to-End Practice

Complete `99-End-to-End-Practice/lab-01-llm-api-wrapper.md`, then upgrade it into a FastAPI endpoint. This is your first portfolio building block.

## Beginner Track

1. Learn what each tool solves before installing anything.
2. Run every code example locally.
3. Rewrite each example once from memory.
4. Keep a small "mistake log" for errors you hit.
5. Explain each concept using the 7-question framework from `learning-rules.md`.

## Advanced Track

1. Add retries, timeouts, and cost logging to every LLM call.
2. Add typed request/response contracts with Pydantic.
3. Add tests around prompt formatting and API behavior.
4. Build one extra endpoint of your own.
5. Prepare a portfolio README with architecture and deployment notes.

## Exit Checklist

- [ ] I can explain what an AI API wrapper is and why production apps need one.
- [ ] I can call an LLM provider with `httpx`.
- [ ] I can validate inputs and outputs with Pydantic v2.
- [ ] I can write async Python without blocking the event loop.
- [ ] I can stream tokens through FastAPI SSE.
- [ ] I can describe the trade-offs of structured outputs.
- [ ] I have a runnable milestone project.
