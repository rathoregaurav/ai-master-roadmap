# M1 Practice: Python for AI Engineering

## Beginner Exercises

1. Modify `pydantic_ai_schemas.py` to add a `max_tokens` field.
2. Make invalid input fail with a clear validation error.
3. Run `async_batch_runner.py` and explain why it finishes faster than serial execution.
4. Add one more fake job.

## Advanced Exercises

1. Add timeout handling to `fake_llm_call`.
2. Return partial results when one job fails.
3. Save results to `results.json`.
4. Add a retry function with exponential backoff.

## Done When

- [ ] You can explain each model field.
- [ ] You can explain `asyncio.gather`.
- [ ] You can show one intentional validation failure.
- [ ] You can describe how this maps to real LLM provider calls.

