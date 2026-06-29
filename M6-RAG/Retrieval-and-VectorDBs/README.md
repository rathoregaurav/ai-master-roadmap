# Retrieval and Vector Databases

## Purpose

Retrieval finds the best evidence for a user query. Vector databases store embeddings and metadata so similarity search can run quickly at scale.

## Concepts

- vector indexes
- metadata filters
- top-k retrieval
- approximate nearest neighbor search
- Qdrant concepts
- pgvector concepts
- hybrid search

## Qdrant vs pgvector

| Tool | Strength | Trade-off |
| --- | --- | --- |
| Qdrant | Purpose-built vector search, filtering, payloads | Extra service to operate |
| pgvector | Keeps vectors near relational data | Scaling and tuning require Postgres skill |

## Best Practices

- Store source metadata with every chunk.
- Keep chunk IDs stable across re-indexing.
- Version embedding models.
- Evaluate before and after index changes.
- Use filters for permissions, tenant, date, and document type.

