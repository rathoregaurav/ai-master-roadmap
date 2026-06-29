# AWS RAG Resource Map

## Purpose

This guide maps common RAG platform needs to AWS services.

| Need | AWS service | Beginner explanation |
| --- | --- | --- |
| Store uploaded files | S3 | durable file storage |
| Trigger ingestion | S3 events / EventBridge | run workflow when something changes |
| Short processing job | Lambda | event-driven function |
| Long processing job | ECS worker | container for heavier work |
| Store metadata | RDS/DynamoDB | document and chunk records |
| Store secrets | Secrets Manager | API keys and passwords |
| Control permissions | IAM | who can do what |
| Run API | ECS/Fargate | containerized FastAPI app |
| Queue work | SQS | buffer async tasks |
| Logs | CloudWatch | logs and metrics |

## Beginner Architecture Choice

Start simple:

- S3 for documents
- ECS for API
- ECS worker for ingestion
- Secrets Manager for keys
- CloudWatch for logs

Add Lambda and SQS when ingestion becomes asynchronous.

