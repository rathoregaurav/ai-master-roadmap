from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AssistantState:
    task: str
    route: str | None = None
    tool_outputs: list[str] = field(default_factory=list)
    final_answer: str = ""


def route_task(task: str) -> str:
    lowered = task.lower()
    if "calculate" in lowered or any(op in lowered for op in ["+", "-", "*", "/"]):
        return "calculator"
    if any(word in lowered for word in ["rag", "agent", "mcp", "memory"]):
        return "knowledge_search"
    if any(word in lowered for word in ["delete", "send", "deploy"]):
        return "approval_required"
    return "direct"


def knowledge_search(task: str) -> str:
    knowledge = {
        "rag": "RAG answers with retrieved evidence.",
        "agent": "Agents use tools and state to complete tasks.",
        "mcp": "MCP is a standard way to expose tools and resources.",
        "memory": "Memory stores useful context across interactions.",
    }
    for key, value in knowledge.items():
        if key in task.lower():
            return value
    return "No matching knowledge found."


def run_assistant(task: str) -> AssistantState:
    state = AssistantState(task=task)
    state.route = route_task(task)

    if state.route == "knowledge_search":
        output = knowledge_search(task)
        state.tool_outputs.append(output)
        state.final_answer = output
    elif state.route == "approval_required":
        state.final_answer = "This task needs human approval before execution."
    elif state.route == "calculator":
        state.final_answer = "Calculator route selected. Add calculator implementation next."
    else:
        state.final_answer = "Direct route selected. Add LLM response generation next."

    return state


if __name__ == "__main__":
    print(run_assistant("Explain RAG before agents"))
