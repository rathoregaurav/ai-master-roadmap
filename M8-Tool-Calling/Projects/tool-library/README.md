# Tool Library - M8 Project

> A reusable library of AI-callable tools following JSON Schema patterns.

## Quick Start

```python
# tools/weather_tool.py
from pydantic import BaseModel, Field
from typing import Optional
import httpx

class WeatherInput(BaseModel):
    location: str = Field(description="City name, e.g. 'San Francisco'")
    unit: str = Field(default="celsius", description="Temperature unit")

class WeatherOutput(BaseModel):
    temperature: float
    condition: str
    humidity: int
    location: str

async def get_weather(args: WeatherInput) -> WeatherOutput:
    """Get current weather for a location."""
    # Mock implementation
    return WeatherOutput(
        temperature=22.5,
        condition="Partly cloudy",
        humidity=65,
        location=args.location
    )

# Tool schema for LLM function calling
WEATHER_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": WeatherInput.model_json_schema()
    }
}
```

## Tool Registry Pattern

```python
# registry.py
from typing import Dict, Callable, Any, Type
from pydantic import BaseModel

class Tool:
    def __init__(self, name: str, description: str, 
                 input_schema: Type[BaseModel],
                 handler: Callable):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.handler = handler
    
    def to_openai_schema(self) -> dict:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.input_schema.model_json_schema()
            }
        }

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool):
        self._tools[tool.name] = tool
    
    def get_schemas(self) -> list:
        return [t.to_openai_schema() for t in self._tools.values()]
    
    async def execute(self, name: str, args: dict) -> Any:
        tool = self._tools.get(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")
        validated = tool.input_schema(**args)
        return await tool.handler(validated)
```

## Project Structure

```
tool-library/
├── registry.py          # Tool registry pattern
├── tools/
│   ├── __init__.py
│   ├── weather.py       # Weather tool
│   ├── calculator.py    # Math calculator
│   ├── database.py      # SQL query tool
│   └── search.py        # Web search tool
├── schemas.py           # Shared schemas
└── examples/
    └── agent_integration.py  # Example with LLM agent