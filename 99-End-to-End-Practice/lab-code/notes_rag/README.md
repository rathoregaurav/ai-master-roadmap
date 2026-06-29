# Notes RAG CLI

## Goal

Ask questions over your own roadmap markdown files using a beginner-friendly retrieval pipeline.

This version uses keyword scoring so you can understand the RAG flow before adding embeddings.

## Run

```bash
python ask_notes.py "What is tool calling?"
```

## What It Teaches

- loading documents
- chunking text
- retrieval scoring
- citations
- answer construction

## Upgrade Path

1. Add embeddings.
2. Add metadata filters.
3. Add query rewriting.
4. Add evaluation cases.
5. Add a FastAPI endpoint.

