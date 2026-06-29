# Structured Output Prompt Example

## Use Case

Extract action items from meeting notes.

## Prompt

```text
You are an operations analyst.

Task:
Extract action items from the meeting notes.

Rules:
- Only include action items explicitly supported by the notes.
- If an owner is missing, use null.
- If a deadline is missing, use null.
- Do not invent tasks.

Meeting notes:
<notes>
{{MEETING_NOTES}}
</notes>

Return valid JSON:
{
  "action_items": [
    {
      "task": "string",
      "owner": "string or null",
      "deadline": "string or null",
      "evidence": "short quote from notes"
    }
  ]
}
```

## Why It Works

- The task is explicit.
- The notes are delimited.
- The output schema is clear.
- The prompt forbids invention.
- Evidence is required, which improves groundedness.

