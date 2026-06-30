# RAG Cheat Sheet

> For interview prep and quick reference. Covers Phase 2 of your roadmap.

## Core RAG Pipeline

```
Documents → Parse → Chunk → Embed → Index → Retrieve → Rerank → LLM → Answer
```

## Chunking Strategies

| Strategy | When | Chunk Size | Overlap |
|----------|------|------------|---------|
| Recursive Character | General text | 500-1000 chars | 10-20% |
| Recursive Token | Code, structured text | 256-512 tokens | 10-20% |
| Semantic | Multi-topic docs | Variable (topic boundaries) | 1 sentence |
| Structure-aware | HTML, Markdown, Legal docs | By heading/section | 0 |
| Sentence-based | FAQs, support tickets | 1-5 sentences | 1 sentence |
| Windowed | Long-form content | 512 tokens | 128 tokens |

## Embedding Models Comparison (2026)

| Model | Dimensions | Max Tokens | Best For | Cost |
|-------|------------|------------|----------|------|
| text-embedding-3-small | 512/1536 | 8191 | General purpose, cheap | $0.02/1M tokens |
| text-embedding-3-large | 256/1024/3072 | 8191 | High accuracy needed | $0.13/1M tokens |
| BGE-M3 (BAAI) | 1024 | 8192 | Multilingual, dense-sparse hybrid | Free (local) |
| Cohere Embed v3 | 1024 | 512 | English, classification + search | $0.10/1M tokens |
| jina-embeddings-v3 | 1024 | 8192 | LoRA adapters, fine-tunable | Free (local) |

## Retrieval Methods

| Method | Speed | Accuracy | Use Case |
|--------|-------|----------|----------|
| Dense (Vector) | Fast | High | Semantic similarity |
| Sparse (BM25) | Fast | Medium | Exact keyword match |
| Hybrid (Dense + Sparse) | Medium | Highest | General purpose |
| Reranking (Cross-encoder) | Slow | Highest | Re-rank top-20 results |

## Search Types

- **Simple Similarity**: cosine distance, L2, dot product
- **Hybrid Search**: BM25 + vector, combined via RRF (Reciprocal Rank Fusion)
- **Multi-Query**: Generate 3-5 query variations, retrieve for each, deduplicate
- **Query Rewriting**: LLM rewrites user query for better retrieval
- **HyDE**: Generate hypothetical document from query, retrieve by its embedding
- **Parent-Child**: Retrieve small child chunks, return parent context
- **Contextual Retrieval**: Include chunk context (document title, previous chunk summary)

## Metrics

| Metric | What It Measures | Formula | Target |
|--------|-----------------|---------|--------|
| Recall@K | Fraction of relevant docs retrieved | relevant_in_topK / total_relevant | > 0.85 |
| MRR | Rank of first relevant doc | 1/rank averaged | > 0.90 |
| Precision@K | How many retrieved are relevant | relevant_in_topK / K | > 0.60 |
| MAP | Average precision across queries | Mean of average precision | > 0.70 |
| NDCG | Rank quality with graded relevance | Normalized discounted cumulative gain | > 0.80 |

## Advanced RAG Techniques

| Technique | What It Does | Complexity | Impact |
|-----------|-------------|------------|--------|
| Query Expansion | Generate similar queries | Low | +5-10% recall |
| Reranking | Cross-encoder re-scoring | Medium | +10-20% precision |
| Context Compression | Condense retrieved chunks | Medium | +10% latency, lower cost |
| Adaptive Retrieval | Retrieve only when needed | High | -30% cost |
| Self-RAG | Self-evaluate retrieved chunks | High | +15% accuracy |
| Corrective RAG | If low scores → rewrite query | Medium | +10% recall |
| Fusion (RRF) | Combine multiple retrievers | Low | +5-10% overall |

## Production Considerations

- **Latency Budget**: Retrieval < 200ms, LLM < 3s, total < 5s
- **Caching**: Exact (Redis) + Semantic (embedding cache)
- **Index Tuning**: HNSW for speed, IVF_PQ for memory
- **Filtering**: Metadata filters before embedding search (date, author, source)
- **Monitoring**: Track empty results rate, retrieval latency, user feedback
- **Cost**: Embedding compute, vector DB storage, LLM generation

## Common Interview Questions

1. "How do you choose chunk size?" → Depends on document type, embedding model max tokens, LLM context window. Evaluate 256, 512, 1024.
2. "Why hybrid search?" → Vector misses exact keyword matches (product codes, names). BM25 misses semantic similarity.
3. "How do you evaluate RAG?" → Golden dataset, Recall@K, MRR, groundedness score.
4. "What happens if retrieval returns nothing?" → Fallback: rewrite query, expand query, or return "no relevant documents found."
5. "How do you handle real-time data?" → Two-tier: pre-indexed (nightly) + hot data (real-time embedding + retrieval).