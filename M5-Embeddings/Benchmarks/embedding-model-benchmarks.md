# Embedding Model Benchmarks

> Performance comparison of popular embedding models. Reference for M5.

## Benchmark Results (MTEB - Massive Text Embedding Benchmark)

| Model | Dimensions | Avg Performance | Clustering | Classification | Reranking | Retrieval | STS |
|-------|------------|-----------------|------------|----------------|-----------|-----------|-----|
| BGE-M3 | 1024 | 64.0 | 48.0 | 75.9 | 60.3 | 52.0 | 82.2 |
| text-embedding-3-large | 3072 | 64.6 | 49.4 | 75.9 | 59.6 | 55.4 | 82.1 |
| text-embedding-3-small | 1536 | 62.3 | 47.7 | 73.5 | 57.5 | 51.9 | 80.5 |
| Cohere Embed v3 | 1024 | 62.0 | 44.9 | 74.0 | 57.0 | 52.0 | 80.0 |
| jina-embeddings-v3 | 1024 | 63.2 | 47.5 | 74.8 | 58.9 | 52.5 | 81.0 |

## Speed Benchmarks (Relative)

| Model | Encoding Speed (docs/sec) | Query Speed (queries/sec) | Memory (GB for 1M docs) |
|-------|--------------------------|--------------------------|------------------------|
| text-embedding-3-small | 500 | 2000 | 6 GB |
| text-embedding-3-large | 150 | 800 | 12 GB |
| BGE-M3 (local) | 200 | 1000 | 8 GB |
| Cohere Embed v3 | 300 | 1500 | 4 GB |
| jina-embeddings-v3 (local) | 250 | 1200 | 6 GB |

## Cost Comparison (1M documents, 512 tokens each)

| Model | Embedding Cost | Storage Cost (1M vectors) | Total |
|-------|---------------|---------------------------|-------|
| text-embedding-3-small | $10.24 | $6.00 | $16.24 |
| text-embedding-3-large | $66.56 | $12.00 | $78.56 |
| BGE-M3 (local) | $0 (compute only) | $8.00 | ~$2.00 (GPU time) |
| Cohere Embed v3 | $51.20 | $4.00 | $55.20 |

## Recommendation

- **Production (cost-sensitive)**: text-embedding-3-small (cheap, good quality)
- **Production (quality-sensitive)**: text-embedding-3-large (best quality)
- **Local/Privacy**: BGE-M3 (free, multilingual, good quality)
- **Classification tasks**: Cohere Embed v3 (optimized for classification)