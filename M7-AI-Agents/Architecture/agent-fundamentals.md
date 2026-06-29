# Agent Fundamentals

## What Is An Agent?

An agent is a program that receives a goal, chooses actions, uses tools, observes results, and decides whether to continue.

## The Simplest Agent Loop

```text
while not done:
    decide next action
    run action
    observe result
    update state
```

## ReAct

ReAct means Reason + Act. The system alternates between thinking about what to do and taking an action through a tool.

In production, you usually do not expose private chain-of-thought. Instead, you store concise decision summaries and tool traces.

## State

Agent state can include:

- original user request
- current plan
- completed steps
- tool results
- errors
- memory references
- final answer

## Exercise

Write a tiny agent that can choose between:

- calculator
- notes search
- final answer

