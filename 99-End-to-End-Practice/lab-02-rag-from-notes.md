# Lab 2: RAG From Your Own Notes

## Goal

Build a RAG system over your roadmap notes.

## Beginner Version

- Load `.md` files.
- Split them into chunks.
- Store chunks in memory.
- Search with keyword overlap.
- Return top chunks with citations.

## Advanced Version

- Add embeddings.
- Add metadata filters by module.
- Add query rewriting.
- Add reranking.
- Add Recall@K evaluation.

## Deliverable

A CLI program:

```bash
python ask_notes.py "What is prompt engineering?"
```

Expected output:

- answer
- source files
- chunk IDs
- confidence or retrieval score

## Practice Questions

- What is RAG?
- Why do agents need tools?
- What is cosine similarity?
- What is structured output?
- How do I evaluate retrieval?

