from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class AgentState:
    user_task: str
    steps: list[str] = field(default_factory=list)
    final_answer: str | None = None


def calculator(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if any(char not in allowed for char in expression):
        return "calculator error: unsupported expression"
    return str(eval(expression, {"__builtins__": {}}, {}))


def search_notes(query: str) -> str:
    notes = {
        "rag": "RAG retrieves external evidence before generation.",
        "agent": "An agent chooses actions, calls tools, and observes results.",
        "mcp": "MCP standardizes how AI clients connect to tools and resources.",
    }
    lowered = query.lower()
    for key, value in notes.items():
        if key in lowered:
            return value
    return "No matching note found."


def decide_next_action(state: AgentState) -> tuple[str, str]:
    task = state.user_task.lower()
    if any(operator in task for operator in ["+", "-", "*", "/"]):
        return "calculator", state.user_task
    if any(word in task for word in ["rag", "agent", "mcp"]):
        return "search_notes", state.user_task
    return "finish", "I can answer this directly after more context."


def run_agent(user_task: str, max_steps: int = 3) -> AgentState:
    state = AgentState(user_task=user_task)
    for _ in range(max_steps):
        action, action_input = decide_next_action(state)
        state.steps.append(f"action={action}, input={action_input}")
        if action == "calculator":
            state.final_answer = calculator(action_input)
            break
        if action == "search_notes":
            state.final_answer = search_notes(action_input)
            break
        state.final_answer = action_input
        break
    if state.final_answer is None:
        state.final_answer = "Stopped because max_steps was reached."
    return state


if __name__ == "__main__":
    result = run_agent("What is RAG?")
    print(result)
