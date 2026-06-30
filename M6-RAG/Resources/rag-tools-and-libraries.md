# RAG Tools & Libraries Reference

> Quick reference for RAG-related tools and libraries. Covers M6.

## Vector Databases Comparison

| Database | Type | Best For | Cloud | Self-Hosted | Cost |
|----------|------|----------|-------|-------------|------|
| pgvector | PostgreSQL extension | Production RAG with existing Postgres | RDS, Aurora | ✅ | Free (add-on) |
| Qdrant | Purpose-built vector DB | High-performance vector search | Qdrant Cloud | ✅ | Free tier available |
| Pinecone | Managed vector DB | Quick start, no ops | ✅ | ❌ | $70/month min |
| Weaviate | Vector + Graph | Hybrid search + knowledge graphs | Weaviate Cloud | ✅ | Free tier available |
| Chroma | Embedded vector DB | Development, prototyping | ❌ | ✅ | Free |
| Milvus | Distributed vector DB | Large-scale (100M+ vectors) | Zilliz Cloud | ✅ | Free tier available |

## Chunking Libraries

| Library | Language | Features |
|---------|----------|----------|
| LangChain Text Splitters | Python | Recursive, semantic, code-aware |
| LlamaIndex Node Parsers | Python | Sentence, token, hierarchical |
| Unstructured.io | Python | PDF, DOCX, HTML, image parsing |
| spaCy Sentence Segmentation | Python | Linguistic sentence boundaries |
| tiktoken | Python | Token counting for OpenAI models |

## Embedding Providers

| Provider | Models | API | Local |
|----------|--------|-----|-------|
| OpenAI | text-embedding-3-small/large | ✅ | ❌ |
| Cohere | embed-english-v3.0, embed-multilingual-v3.0 | ✅ | ❌ |
| BAAI BGE | BGE-M3, BGE-small, BGE-large | ❌ | ✅ |
| Sentence Transformers | all-MiniLM-L6-v2, all-mpnet-base-v2 | ❌ | ✅ |
| Jina AI | jina-embeddings-v3 | ✅ | ✅ |
| Voyage AI | voyage-2, voyage-large-2 | ✅ | ❌ |

## RAG Frameworks

| Framework | Strengths | Weaknesses |
|-----------|-----------|------------|
| LangChain | Broad ecosystem, many integrations | Complex, breaking changes |
| LlamaIndex | Best for RAG, great evaluation tools | Steeper learning curve |
| Haystack | Modular, production-ready | Smaller community |
| DSPy | Programmatic prompt optimization | Different paradigm, learning curve |

## Evaluation Tools

| Tool | What It Evaluates |
|------|-------------------|
| RAGAS | Faithfulness, answer relevance, context precision/recall |
| LangSmith | Traces, evals, dataset management |
| Arize AI | Production monitoring, drift detection |
| DeepEval | Unit testing for LLM outputs |
| MLflow | Experiment tracking, model registry |