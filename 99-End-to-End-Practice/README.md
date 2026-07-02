# End-to-End Practice

This folder connects all modules into complete practice work. Each lab forces you to build something real instead of only reading notes.

## Practice Ladder

| Lab | Level | What you build |
| --- | --- | --- |
| Lab 1 | Beginner | LLM API wrapper |
| Lab 2 | Beginner | Text RAG over local notes |
| Lab 3 | Beginner/Intermediate | Agentic assistant with tools |
| Lab 4 | Intermediate | Production hardening |
| Lab 5 | Intermediate | Enterprise AI platform layer |
| Lab 6 | Intermediate | Evaluated RAG platform |
| Lab 7 | Advanced | Tool-calling operations assistant |
| Lab 8 | Advanced | Memory + MCP + evaluation integration |

## Runnable Starter Labs

- `lab-code/notes_rag/ask_notes.py`: ask questions over the roadmap markdown files.
- `lab-code/beginner_agent/agent.py`: route beginner agent tasks to tools.
- `lab-code/production_hardening/harden_ai_request.py`: practice observability, security, routing, and cost checks.
- `lab-code/enterprise_platform/enterprise_control_plane.py`: practice registries, feature flags, audit, lineage, and tenants.

## How To Use Labs

Each lab should produce:

- source code
- README
- diagram
- sample inputs
- sample outputs
- tests or evaluation cases
- reflection notes
- security and privacy notes
- cost and latency notes
- failure-mode notes

## Enterprise Lab Rubric

Use this rubric before marking any lab complete:

| Area | Minimum standard |
| --- | --- |
| Learning | You can explain the main pattern in under two minutes. |
| Code | The happy path runs locally or has a documented dry run. |
| Tests/eval | At least three test cases or eval cases exist. |
| Security | Inputs, secrets, and tool permissions are considered. |
| Observability | Logs or traces show the important steps. |
| Interview | You can describe architecture, trade-offs, and failure modes. |
| Portfolio | The README has setup, usage, diagram, and limitations. |

## Rule

Do not mark a lab complete until you can demo it in under five minutes.
