# AI Testing Framework

Testing strategies for AI systems.

## Testing Levels

| Level | What | Tool |
|-------|------|------|
| **Unit** | Individual functions, parsers, chunkers | pytest |
| **Integration** | API endpoints, database queries | pytest + httpx |
| **Prompt Regression** | LLM responses stay consistent | LLM-as-Judge |
| **Golden Dataset** | Known Q&A pairs | Custom framework |
| **Load** | System under concurrent users | Locust |
| **Chaos** | Service failures | Chaos Mesh |

## Resources

See [PHASE-8-STAFF-AI-ADDENDUM.md](../PHASE-8-STAFF-AI-ADDENDUM.md) Section 3 for:
- Prompt Regression Testing
- Mock LLM implementation
