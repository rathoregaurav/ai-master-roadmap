from dataclasses import dataclass


@dataclass(frozen=True)
class Resource:
    uri: str
    name: str
    content: str


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict


class MCPStyleServer:
    def __init__(self) -> None:
        self.resources = {
            "notes://rag": Resource(
                uri="notes://rag",
                name="RAG notes",
                content="RAG retrieves evidence before generation.",
            )
        }
        self.tools = {
            "echo": ToolSpec(
                name="echo",
                description="Return the input message.",
                input_schema={"type": "object", "required": ["message"]},
            )
        }

    def list_resources(self) -> list[Resource]:
        return list(self.resources.values())

    def read_resource(self, uri: str) -> Resource:
        return self.resources[uri]

    def list_tools(self) -> list[ToolSpec]:
        return list(self.tools.values())

    def call_tool(self, name: str, arguments: dict) -> dict:
        if name == "echo":
            return {"message": arguments["message"]}
        return {"error": "unknown tool"}


if __name__ == "__main__":
    server = MCPStyleServer()
    print(server.list_resources())
    print(server.call_tool("echo", {"message": "hello MCP"}))

