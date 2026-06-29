from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    function: Callable[[dict], dict]
    required_args: set[str]


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def call(self, name: str, arguments: dict) -> dict:
        if name not in self.tools:
            return {"ok": False, "error": f"unknown tool: {name}"}
        tool = self.tools[name]
        missing = tool.required_args - set(arguments)
        if missing:
            return {"ok": False, "error": f"missing arguments: {sorted(missing)}"}
        try:
            return {"ok": True, "data": tool.function(arguments)}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}


def calculator(arguments: dict) -> dict:
    a = float(arguments["a"])
    b = float(arguments["b"])
    operation = arguments["operation"]
    if operation == "add":
        return {"result": a + b}
    if operation == "multiply":
        return {"result": a * b}
    raise ValueError("unsupported operation")


if __name__ == "__main__":
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="calculator",
            description="Perform safe arithmetic.",
            function=calculator,
            required_args={"a", "b", "operation"},
        )
    )
    print(registry.call("calculator", {"a": 2, "b": 3, "operation": "multiply"}))

