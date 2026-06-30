# AWS Document Processing Pipeline - M16 Project

> Serverless document processing pipeline using AWS services for async ingestion.

## Architecture

```
S3 Upload → SQS Queue → Lambda Worker → (OCR → Chunk → Embed → Store) → pgvector / OpenSearch
```

## Infrastructure (Terraform/Pulumi reference)

```hcl
# main.tf - Key resources
resource "aws_s3_bucket" "documents" {
  bucket = "ai-doc-ingestion-raw"
}

resource "aws_sqs_queue" "doc_processing" {
  name                        = "doc-processing-queue"
  visibility_timeout_seconds  = 300
  message_retention_seconds   = 86400
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.doc_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_sqs_queue" "doc_dlq" {
  name = "doc-processing-dlq"
}

resource "aws_lambda_function" "doc_processor" {
  function_name = "doc-processor"
  runtime       = "python3.12"
  handler       = "handler.lambda_handler"
  filename      = "lambda_function_payload.zip"
  timeout       = 300  # 5 minutes
  memory_size   = 1024
  
  environment {
    variables = {
      EMBEDDING_ENDPOINT = "https://your-embedding-api.com"
      VECTOR_DB_HOST     = "your-pgvector-host"
    }
  }
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.doc_processing.arn
  function_name    = aws_lambda_function.doc_processor.function_name
  batch_size       = 1
}
```

## Lambda Handler

```python
# handler.py
import json
import boto3
from urllib.parse import urlparse

s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        body = json.loads(record['body'])
        
        # Get document from S3
        bucket = body['bucket']
        key = body['key']
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        
        # Process: OCR → Chunk → Embed → Store
        chunks = chunk_document(content)
        embeddings = embed_chunks(chunks)
        store_vectors(chunks, embeddings)
        
        # Update document status
        update_status(bucket, key, "processed")
    
    return {"statusCode": 200, "body": json.dumps("Success")}
```

## Project Structure

```
aws-doc-processing/
├── handler.py             # Lambda function handler
├── terraform/             # Infrastructure as code
│   ├── main.tf
│   └── variables.tf
├── scripts/               # Utility scripts
│   ├── upload_test_doc.sh
│   └── check_status.sh
├── requirements.txt
└── README.md