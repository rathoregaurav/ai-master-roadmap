# AI Agents Cheat Sheet

> Quick reference for agent architectures, patterns, and interview prep. Covers Phase 3.

## Agent Loop (ReAct)

```
1. Observe user input / tool result
2. Think: What step to take next?
3. Act: Call a tool or generate response
4. Observe tool result
5. Repeat until task complete or stop condition met
```

## Core Agent Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| **ReAct** | Interleave reasoning + tool calls | Default for most agents |
| **Router** | Classify input → route to handler | Customer support ticketing |
| **Supervisor** | Delegate tasks, monitor workers, intervene | Multi-agent systems |
| **Reflection** | Generate → Self-critique → Improve | High-quality content generation |
| **Critic** | One agent generates, another critiques | Legal review, code review |
| **Debate** | Multiple agents debate → Consensus | Decision-making, fact-checking |
| **Planner-Executor** | Plan steps → Execute each → Adapt | Multi-step tasks (travel booking) |
| **Tool-using** | LLM decides which tool(s) to call | Data analysis, API orchestration |

## Stopping Conditions

1. **Task Complete**: Agent outputs final answer
2. **Max Iterations**: Hard limit (e.g., 20 steps)
3. **Time Budget**: Stop after N seconds
4. **Human Interrupt**: User cancels or approves
5. **Critical Error**: Unrecoverable tool failure
6. **Low Confidence**: Model uncertainty > threshold
7. **Budget Exhausted**: Token/cost limit hit
8. **Loop Detection**: Same action repeated > N times

## Memory Types in Agents

| Type | Storage | Retrieval | Eviction |
|------|---------|-----------|----------|
| Working (session) | LLM context | All in prompt | Session ends |
| Episodic (events) | Vector DB | Embedding similarity | Time-decay + LRU |
| Semantic (facts) | KV store / Graph | Exact + semantic | Confidence < threshold |
| Procedural (skills) | Prompt templates | Task matching | Manual versioning |

## Tool Design Principles

- **Narrow scope**: Each tool does one thing well
- **Validation**: Pydantic schema for every argument
- **Permissions**: Read vs Write scoping
- **Error recovery**: Return structured errors for LLM correction
- **Audit**: Log every call (user, input, output, timestamp)
- **Rate limits**: Per user, per tool
- **Timeouts**: Abort calls exceeding N seconds

## Production Agent Checklist

- [ ] Max iteration limit
- [ ] Time budget per task
- [ ] Human approval gates for destructive actions
- [ ] State checkpoints for crash recovery
- [ ] Audit log of every action
- [ ] Evaluation of task completion rate
- [ ] Circuit breaker for failing tools
- [ ] Graceful degradation when tools fail
- [ ] Prompt injection guards on tool calls
- [ ] PII scrub on tool inputs/outputs

## Common Anti-Patterns

| Anti-Pattern | Why Bad | Fix |
|-------------|---------|-----|
| No max iterations | Infinite loops possible | Set hard limit + time budget |
| Overly broad tools | Agent can do anything | Narrow each tool scope |
| Trusting tool output blindly | Tool failure → wrong reasoning | Validate + return structured errors |
| No human review for writes | Destructive actions possible | Approval gate pattern |
| Single agent for everything | Confusion, poor specialization | Supervisor + worker pattern |
| No memory limits | Memory grows unbounded | Eviction + compression policies |
| Missing stopping conditions | Runaway costs | All 8 stopping conditions above |

## Key Metrics

| Metric | Definition | Target |
|--------|------------|--------|
| Task Success Rate | % of tasks completed successfully | > 85% |
| Average Steps | Steps per completed task | Minimize |
| Tool Accuracy | Correct tool called for the task | > 90% |
| Human Intervention Rate | % of tasks needing human help | < 10% |
| Cost Per Task | Tokens + API calls per task | Budget-dependent |
| Error Recovery Rate | % of tool failures agent recovered from | > 70% |