from dataclasses import dataclass


@dataclass(frozen=True)
class AgentEvalCase:
    user_task: str
    expected_route: str
    expected_contains: str


def fake_agent(task: str) -> dict[str, str]:
    lowered = task.lower()
    if "rag" in lowered:
        return {"route": "knowledge_search", "answer": "RAG retrieves evidence."}
    if "+" in lowered:
        return {"route": "calculator", "answer": "calculator selected"}
    return {"route": "direct", "answer": "direct answer"}


def evaluate_case(case: AgentEvalCase) -> dict[str, object]:
    result = fake_agent(case.user_task)
    route_ok = result["route"] == case.expected_route
    answer_ok = case.expected_contains.lower() in result["answer"].lower()
    return {
        "task": case.user_task,
        "route_ok": route_ok,
        "answer_ok": answer_ok,
        "passed": route_ok and answer_ok,
        "result": result,
    }


if __name__ == "__main__":
    cases = [
        AgentEvalCase("What is RAG?", "knowledge_search", "evidence"),
        AgentEvalCase("2 + 2", "calculator", "calculator"),
    ]
    for case in cases:
        print(evaluate_case(case))

