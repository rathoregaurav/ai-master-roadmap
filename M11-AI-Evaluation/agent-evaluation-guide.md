# Agent Evaluation Guide

## What To Evaluate

Agent evaluation is not only final answer quality. You must evaluate the path the agent took.

## Agent Metrics

| Metric | Meaning |
| --- | --- |
| route accuracy | did the agent choose the right worker/tool? |
| tool accuracy | did it call the correct tool? |
| argument validity | were tool arguments valid? |
| task success | did the task complete? |
| step count | did it finish efficiently? |
| safety | did it avoid unsafe actions? |
| recovery | did it handle errors well? |

## Golden Dataset Format

```json
{
  "task": "What is RAG?",
  "expected_route": "knowledge_search",
  "expected_tools": ["search_notes"],
  "expected_answer_contains": ["retrieval", "evidence"],
  "unsafe_actions_allowed": false
}
```

## Beginner Practice

Create 10 agent test cases:

- 3 knowledge questions
- 2 calculator tasks
- 2 approval-required tasks
- 2 direct answer tasks
- 1 impossible task

## Advanced Practice

Track:

- pass rate by route
- common failure reason
- average step count
- unsafe action count
- regression from previous run

