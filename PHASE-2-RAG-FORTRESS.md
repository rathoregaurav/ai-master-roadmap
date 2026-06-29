# Phase 2: The RAG Fortress

Goal: master retrieval-augmented generation deeply enough to build systems you can evaluate, debug, and improve.

RAG is not "put PDFs into a vector database." RAG is an engineering system that transforms messy source material into retrievable evidence, retrieves the right evidence under realistic constraints, and proves the answer is grounded.

For your AI transition, Phase 2 is the most important bridge from beginner to real-world AI engineer. Many production AI jobs are RAG-heavy because companies need AI over private documents, policies, support tickets, contracts, and internal knowledge.

## Weekly Plan

| Week | Modules | Main outcome |
| --- | --- | --- |
| 4 | M5 + M6 document processing | Embeddings, chunking, and ingestion pipeline |
| 5 | M6 retrieval/vector DBs | Search, filters, hybrid retrieval, Qdrant/pgvector concepts |
| 6 | M6 advanced RAG | Query rewriting, multi-query, reranking, context compression |
| 7 | M6 evaluation | Golden datasets, Recall@K, MRR, groundedness checks |

## Phase Deliverable

Build the `Enterprise RAG Platform`: a local RAG app with:

- document ingestion
- chunking and metadata
- vector-style search
- keyword fallback
- reranking
- answer generation interface
- evaluation dashboard data

Starter project: `M6-RAG/Projects/enterprise-rag-platform/`

## End-to-End Practice

Complete `99-End-to-End-Practice/lab-02-rag-from-notes.md`, then run the starter CLI in `99-End-to-End-Practice/lab-code/notes_rag/`.

## Beginner Track

1. Implement cosine similarity from scratch.
2. Chunk plain text before trying PDFs.
3. Build a tiny in-memory vector index.
4. Evaluate retrieval with 5 hand-written questions.
5. Only then move to a real vector database.

## Advanced Track

1. Compare chunk sizes and overlaps.
2. Add metadata filtering.
3. Add hybrid lexical + vector scoring.
4. Add reranking and context compression.
5. Track Recall@K, MRR, answer groundedness, latency, and cost.

## Exit Checklist

- [ ] I can explain embeddings, vector similarity, and semantic search.
- [ ] I can design a chunking strategy for PDFs, DOCX, HTML, and support tickets.
- [ ] I can compare vector DB options without hype.
- [ ] I can implement hybrid retrieval and reranking.
- [ ] I can build a golden dataset.
- [ ] I can calculate Recall@K and MRR.
- [ ] I can debug a bad RAG answer by inspecting retrieval evidence.
