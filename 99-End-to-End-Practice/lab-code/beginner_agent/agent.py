from __future__ import annotations

import sys
from dataclasses import dataclass, field


@dataclass
class AgentTrace:
    task: str
    route: str
    observations: list[str] = field(default_factory=list)
    final_answer: str = ""


def route(task: str) -> str:
    lowered = task.lower()
    if lowered.startswith("calculate") or any(op in lowered for op in [" + ", " - ", " * ", " / "]):
        return "calculator"
    if any(word in lowered for word in ["rag", "agent", "tool", "mcp", "memory", "evaluation"]):
        return "knowledge"
    if any(word in lowered for word in ["delete", "send", "deploy", "purchase"]):
        return "approval"
    return "direct"


def calculator(task: str) -> str:
    expression = task.lower().replace("calculate", "").strip()
    allowed = set("0123456789+-*/(). ")
    if not expression or any(char not in allowed for char in expression):
        return "Calculator needs a simple numeric expression."
    return f"Result: {eval(expression, {'__builtins__': {}}, {})}"


def knowledge(task: str) -> str:
    notes = {
        "rag": "RAG retrieves evidence before generation.",
        "agent": "An agent chooses actions, calls tools, observes results, and stops when done.",
        "tool": "Tool calling lets an AI system request structured external actions.",
        "mcp": "MCP standardizes how AI clients connect to tools and resources.",
        "memory": "Memory stores useful context for future interactions.",
        "evaluation": "Evaluation measures AI behavior and catches regressions.",
    }
    lowered = task.lower()
    matches = [value for key, value in notes.items() if key in lowered]
    return " ".join(matches) if matches else "No matching knowledge found."


def run_agent(task: str) -> AgentTrace:
    selected_route = route(task)
    trace = AgentTrace(task=task, route=selected_route)

    if selected_route == "calculator":
        trace.observations.append("Using calculator tool.")
        trace.final_answer = calculator(task)
    elif selected_route == "knowledge":
        trace.observations.append("Using knowledge lookup tool.")
        trace.final_answer = knowledge(task)
    elif selected_route == "approval":
        trace.observations.append("Risky action detected.")
        trace.final_answer = "Human approval is required before this action can run."
    else:
        trace.observations.append("Using direct response route.")
        trace.final_answer = "I need more specific AI context, but this route is ready for an LLM call."

    return trace


def main() -> None:
    task = " ".join(sys.argv[1:]).strip() or "What is an agent?"
    trace = run_agent(task)
    print(trace)


if __name__ == "__main__":
    main()

