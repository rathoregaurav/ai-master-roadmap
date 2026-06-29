# AI Security Checklist

## Input Security

- [ ] Validate request shape.
- [ ] Limit input length.
- [ ] Detect prompt injection patterns.
- [ ] Treat retrieved documents as untrusted data.
- [ ] Separate instructions from user-provided content.

## Data Security

- [ ] Do not log raw secrets.
- [ ] Scrub obvious PII.
- [ ] Use tenant/user filters in retrieval.
- [ ] Store only necessary data.
- [ ] Document what data is sent to model providers.

## Tool Security

- [ ] Give tools narrow permissions.
- [ ] Validate tool arguments.
- [ ] Add read/write/destructive risk labels.
- [ ] Require human approval for write/destructive tools.
- [ ] Log tool calls and results.

## Output Security

- [ ] Validate structured outputs.
- [ ] Block secrets and private data in final response.
- [ ] Add citations for RAG answers.
- [ ] Add refusal behavior for unsupported risky tasks.

## Production Security

- [ ] Add rate limits.
- [ ] Add audit logs.
- [ ] Add alerting for repeated attacks.
- [ ] Test known prompt injection examples.
- [ ] Review dependencies and deployment secrets.

