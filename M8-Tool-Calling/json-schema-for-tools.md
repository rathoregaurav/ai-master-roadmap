# JSON Schema For Tools

## Beginner Explanation

A tool schema tells the model exactly what arguments a tool accepts. Without a schema, the model may call a tool with missing, misspelled, or unsafe arguments.

## Example

```json
{
  "type": "object",
  "required": ["city", "unit"],
  "properties": {
    "city": {
      "type": "string",
      "description": "City name, such as Mumbai or San Francisco"
    },
    "unit": {
      "type": "string",
      "enum": ["celsius", "fahrenheit"]
    }
  }
}
```

## What To Validate

- required fields
- field types
- allowed values
- string length
- numeric ranges
- permission level
- user authorization

## Beginner Practice

Create a schema for:

- calculator
- notes search
- create calendar event
- search customer record

## Advanced Practice

Design a tool schema that prevents destructive database actions unless `approval_id` is present.

## Interview Questions

1. Why is a schema better than a natural language tool description alone?
2. What can still go wrong after schema validation?
3. Why should write tools have stricter validation than read tools?

