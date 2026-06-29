# MCP Safety And Enterprise Design

## Why Enterprises Care

Enterprises have many internal systems: documents, tickets, calendars, databases, repositories, dashboards, and APIs. MCP helps expose these capabilities in a standard way, but the security model still matters.

## Tools vs Resources

| Capability | Meaning | Risk |
| --- | --- | --- |
| Resource | read context | lower |
| Tool | perform action or compute | medium/high |
| Prompt | reusable instruction template | low/medium |

## Enterprise Controls

- authentication
- authorization
- tenant isolation
- audit logs
- rate limits
- approval gates
- data classification
- least-privilege tools

## Beginner Design Exercise

Design an MCP-style server for your learning roadmap:

- resource: `roadmap://phase-1`
- resource: `roadmap://phase-2`
- resource: `roadmap://phase-3`
- tool: `search_notes`
- tool: `create_study_plan`

## Advanced Design Exercise

Add a permission model:

- public resources
- private resources
- read-only tools
- approval-required tools

