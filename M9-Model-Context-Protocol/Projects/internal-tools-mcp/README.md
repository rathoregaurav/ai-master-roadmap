# Internal Tools MCP Server

> MCP server that exposes internal company tools (Slack, Jira, GitHub, calendar) via the Model Context Protocol.

## Quick Start

```python
# server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json

# Define tools
async def list_jira_tickets() -> list[dict]:
    # Mock implementation
    return [{"id": "PROJ-123", "title": "Fix login bug", "status": "Open"}]

async def send_slack_message(channel: str, message: str) -> dict:
    # Mock implementation  
    return {"ok": True, "channel": channel, "ts": "1234567890.123"}

# Create MCP server
server = Server("internal-tools")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_jira_tickets",
            description="List JIRA tickets assigned to the user",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string", "description": "Project key (optional)"}
                }
            }
        ),
        Tool(
            name="send_slack_message",
            description="Send a message to a Slack channel",
            inputSchema={
                "type": "object",
                "properties": {
                    "channel": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["channel", "message"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "list_jira_tickets":
        tickets = await list_jira_tickets()
        return [TextContent(type="text", text=json.dumps(tickets, indent=2))]
    elif name == "send_slack_message":
        result = await send_slack_message(**arguments)
        return [TextContent(type="text", text=json.dumps(result))]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Project Structure

```
internal-tools-mcp/
├── server.py              # MCP server entry point
├── tools/
│   ├── slack.py           # Slack integration
│   ├── jira.py            # JIRA integration
│   ├── github.py          # GitHub integration
│   └── calendar.py        # Calendar integration
├── auth.py                # Authentication for tools
├── requirements.txt
└── README.md