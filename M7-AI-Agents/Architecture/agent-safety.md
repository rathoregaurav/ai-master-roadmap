# Agent Safety

## Why Agent Safety Matters

Agents can take multiple steps. A small mistake in one step can compound into a larger failure. The more tools an agent has, the more careful the safety design must be.

## Safety Layers

| Layer | Purpose |
| --- | --- |
| Input validation | reject malformed or unsafe requests |
| Tool permissions | restrict what actions are allowed |
| Approval gates | pause before risky actions |
| Max iterations | prevent infinite loops |
| Audit logs | preserve what happened |
| Evaluation | catch repeated failure patterns |

## Risk Levels

| Risk | Example | Required control |
| --- | --- | --- |
| Low | search notes | logging |
| Medium | query database | auth and filtering |
| High | send email | approval |
| Critical | delete production data | approval, audit, rollback |

## Beginner Rule

Read-only tools first. Write tools later.

## Practice

Add a risk label to every tool:

- `read`
- `compute`
- `write`
- `destructive`

Then require approval for `write` and `destructive`.

