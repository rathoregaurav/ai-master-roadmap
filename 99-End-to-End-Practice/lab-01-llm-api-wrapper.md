# Lab 1: LLM API Wrapper

## Goal

Build a clean Python wrapper around an LLM API or fake LLM service.

## Beginner Version

- Create a `PromptRequest` model.
- Create a `PromptResponse` model.
- Write a function called `generate_response`.
- Return a fake answer first.
- Log the request ID.

## Advanced Version

- Add provider timeouts.
- Add retries.
- Add cost estimate fields.
- Add structured output validation.
- Add unit tests with mocked responses.

## Deliverable

A folder containing:

- `client.py`
- `schemas.py`
- `README.md`
- `examples/basic_call.py`

## Reflection Questions

1. Why should AI provider calls be wrapped?
2. What should happen when the provider fails?
3. What fields should be logged?
4. What should never be logged?

