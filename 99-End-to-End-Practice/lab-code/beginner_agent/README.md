# Beginner Agent CLI

## Goal

Build a beginner agent that routes tasks to simple tools.

This is intentionally plain Python. Learn the loop first, then move to frameworks.

## Run

```bash
python agent.py "What is RAG?"
python agent.py "calculate 2 + 3"
python agent.py "delete old records"
```

## What It Teaches

- routing
- tools
- state
- approval gates
- final answer generation

## Upgrade Path

1. Add a real calculator parser.
2. Add notes RAG as a tool.
3. Add memory.
4. Add eval cases.
5. Replace router rules with an LLM router.

