# Lab 3: Agentic Assistant

## Goal

Build an assistant that can decide whether to answer directly, search notes, call a calculator, or ask for clarification.

## Beginner Version

Use simple if/else routing:

- math question -> calculator
- roadmap question -> notes search
- unclear question -> clarification
- general question -> direct answer

## Advanced Version

Use an agent loop:

1. Observe user request.
2. Decide next action.
3. Call tool.
4. Observe tool result.
5. Decide whether to finish.

## Deliverable

A working CLI:

```bash
python agent.py "What should I learn before MCP?"
```

## Evaluation

Create 10 test tasks:

- 3 direct answer tasks
- 3 retrieval tasks
- 2 calculator tasks
- 2 unclear tasks

Track:

- correct route
- correct answer
- tool errors
- final response quality

