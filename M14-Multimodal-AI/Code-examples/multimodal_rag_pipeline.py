"""
M14: Multimodal RAG Pipeline
=============================
End-to-end RAG that handles both text and images.

Key skills:
- Chunking documents with embedded images
- Storing image references alongside text chunks
- Retrieving both text and image context
- Generating answers with visual citations
- Handling PDFs with mixed content
"""

import base64
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1. Data Models
# ──────────────────────────────────────────────

class TextChunk(BaseModel):
    """A text chunk with optional image references."""
    id: str
    text: str
    source: str
    page_number: Optional[int] = None
    image_refs: list[str] = Field(default_factory=list, description="Base64 image references")


class RetrievedChunk(BaseModel):
    """A chunk returned from retrieval."""
    chunk: TextChunk
    score: float
    modality: str = "text"  # "text" or "image"


class MultimodalQueryResult(BaseModel):
    """Final answer with citations."""
    answer: str
    supporting_chunks: list[RetrievedChunk]
    visual_evidence: list[str] = Field(default_factory=list, description="Base64 images used")


# ──────────────────────────────────────────────
# 2. Document Processor
# ──────────────────────────────────────────────

class DocumentProcessor:
    """Process documents into multimodal chunks."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_text_file(self, file_path: str, source: str = "") -> list[TextChunk]:
        """Split a text file into chunks."""
        path = Path(file_path)
        text = path.read_text(encoding="utf-8")
        source = source or path.name
        return self._chunk_text(text, source)

    def process_markdown_with_images(
        self, file_path: str, image_dir: Optional[str] = None
    ) -> list[TextChunk]:
        """
        Process a markdown file, extracting image references.
        
        In a real system, you'd:
        1. Parse the markdown AST
        2. Extract image paths
        3. Encode images as base64
        4. Attach them to nearby text chunks
        """
        path = Path(file_path)
        text = path.read_text(encoding="utf-8")
        source = path.name
        chunks = self._chunk_text(text, source)

        # Simple image extraction: find markdown image syntax
        import re
        image_pattern = re.compile(r"!\[.*?\]\((.*?)\)")
        all_images = image_pattern.findall(text)

        if image_dir:
            for chunk in chunks:
                # Find images that appear in this chunk's text
                chunk_images = image_pattern.findall(chunk.text)
                for img_path in chunk_images:
                    full_path = Path(image_dir) / img_path
                    if full_path.exists():
                        b64 = base64.b64encode(full_path.read_bytes()).decode("utf-8")
                        chunk.image_refs.append(b64)

        return chunks

    def _chunk_text(self, text: str, source: str) -> list[TextChunk]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        chunk_id = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            # Try to break at a sentence boundary
            if end < len(text):
                # Look for sentence end within the last 20% of the chunk
                search_start = max(start, end - self.chunk_size // 5)
                last_period = text.rfind(". ", search_start, end)
                last_newline = text.rfind("\n\n", search_start, end)
                break_point = max(last_period, last_newline)
                if break_point > search_start:
                    end = break_point + 1

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(TextChunk(
                    id=f"chunk_{chunk_id:04d}",
                    text=chunk_text,
                    source=source,
                ))
                chunk_id += 1

            # Move start with overlap
            start = end - self.chunk_overlap if end < len(text) else len(text)

        logger.info(f"Created {len(chunks)} chunks from {source}")
        return chunks


# ──────────────────────────────────────────────
# 3. Simple Vector Store (In-Memory)
# ──────────────────────────────────────────────

@dataclass
class SimpleVectorStore:
    """Minimal in-memory vector store for demo purposes."""
    chunks: list[TextChunk] = field(default_factory=list)
    _embeddings: dict[str, list[float]] = field(default_factory=dict)

    def add_chunks(self, chunks: list[TextChunk], embeddings: list[list[float]]):
        for chunk, emb in zip(chunks, embeddings):
            self.chunks.append(chunk)
            self._embeddings[chunk.id] = emb

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[RetrievedChunk]:
        """Simple cosine similarity search."""
        import math

        def cosine_sim(a: list[float], b: list[float]) -> float:
            dot = sum(x * y for x, y in zip(a, b))
            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(x * x for x in b))
            return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

        scored = []
        for chunk in self.chunks:
            if chunk.id in self._embeddings:
                score = cosine_sim(query_embedding, self._embeddings[chunk.id])
                scored.append(RetrievedChunk(chunk=chunk, score=score))

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]


# ──────────────────────────────────────────────
# 4. Embedding Client
# ──────────────────────────────────────────────

class EmbeddingClient:
    """Get embeddings for text."""

    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        self.api_key = api_key
        self.model = model
        self.client = httpx.Client(timeout=30.0)

    def embed(self, text: str) -> list[float]:
        """Get embedding for a single text."""
        response = self.client.post(
            "https://api.openai.com/v1/embeddings",
            json={"input": text, "model": self.model},
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for multiple texts."""
        response = self.client.post(
            "https://api.openai.com/v1/embeddings",
            json={"input": texts, "model": self.model},
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        response.raise_for_status()
        data = response.json()["data"]
        data.sort(key=lambda x: x["index"])
        return [d["embedding"] for d in data]

    def close(self):
        self.client.close()


# ──────────────────────────────────────────────
# 5. Multimodal RAG Pipeline
# ──────────────────────────────────────────────

class MultimodalRAG:
    """
    End-to-end multimodal RAG pipeline.
    
    Ingests documents → indexes chunks + images → retrieves relevant context → generates answer.
    """

    def __init__(self, openai_api_key: str):
        self.api_key = openai_api_key
        self.embedder = EmbeddingClient(api_key=openai_api_key)
        self.vector_store = SimpleVectorStore()
        self.llm_client = httpx.Client(timeout=60.0)
        self.processor = DocumentProcessor()

    def ingest_text(self, file_path: str, source: str = ""):
        """Ingest a text file into the vector store."""
        chunks = self.processor.process_text_file(file_path, source)
        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed_batch(texts)
        self.vector_store.add_chunks(chunks, embeddings)
        logger.info(f"Ingested {len(chunks)} chunks from {source or file_path}")

    def ingest_markdown_with_images(self, file_path: str, image_dir: Optional[str] = None):
        """Ingest markdown with embedded images."""
        chunks = self.processor.process_markdown_with_images(file_path, image_dir)
        texts = [c.text for c in chunks]
        embeddings = self.embedder.embed_batch(texts)
        self.vector_store.add_chunks(chunks, embeddings)
        logger.info(f"Ingested {len(chunks)} multimodal chunks from {file_path}")

    def query(self, question: str, top_k: int = 5) -> MultimodalQueryResult:
        """
        Answer a question using multimodal RAG.
        
        1. Embed the question
        2. Retrieve relevant chunks
        3. Build context with images
        4. Generate answer with LLM
        """
        # Step 1: Embed question
        query_emb = self.embedder.embed(question)

        # Step 2: Retrieve
        retrieved = self.vector_store.search(query_emb, top_k=top_k)

        # Step 3: Build context
        text_context = "\n\n".join(
            f"[Chunk {r.chunk.id} from {r.chunk.source} (score: {r.score:.3f})]\n{r.chunk.text}"
            for r in retrieved
        )

        # Collect visual evidence
        visual_evidence = []
        for r in retrieved:
            visual_evidence.extend(r.chunk.image_refs)

        # Step 4: Generate answer
        prompt = f"""You are a multimodal research assistant. Answer the question based on the provided context.

Context:
{text_context}

Question: {question}

Provide a comprehensive answer. If the context includes images, reference them in your answer.
Return JSON with: answer (string), supporting_sources (list of chunk IDs used).
"""

        try:
            response = self.llm_client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You answer questions using provided context."},
                        {"role": "user", "content": prompt},
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens": 2000,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            result = json.loads(data["choices"][0]["message"]["content"])

            return MultimodalQueryResult(
                answer=result.get("answer", ""),
                supporting_chunks=retrieved,
                visual_evidence=visual_evidence[:3],  # Limit to 3 images
            )

        except Exception as e:
            logger.error(f"Query failed: {e}")
            raise

    def close(self):
        self.embedder.close()
        self.llm_client.close()


# ──────────────────────────────────────────────
# 6. Demo
# ──────────────────────────────────────────────

def demo():
    """Run a demo of the multimodal RAG pipeline."""
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("No OPENAI_API_KEY set. Skipping demo.")
        logger.info("To run: export OPENAI_API_KEY='your-key'")
        return

    rag = MultimodalRAG(api_key)

    # Create a sample document
    sample_dir = Path("/tmp/multimodal_rag_demo")
    sample_dir.mkdir(exist_ok=True)
    
    doc_path = sample_dir / "sample_doc.md"
    doc_path.write_text("""
# AI Engineering Guide

## RAG Systems
Retrieval-Augmented Generation (RAG) is a technique that combines 
information retrieval with text generation. It allows LLMs to access 
external knowledge bases.

## Multimodal AI
Multimodal systems can process text, images, and audio simultaneously.
GPT-4o and Claude 3.5 are leading multimodal models.

## Vector Databases
Vector databases store embeddings for efficient similarity search.
Popular options include Qdrant, Pinecone, and pgvector.
    """)

    try:
        # Ingest
        logger.info("Ingesting sample document...")
        rag.ingest_text(str(doc_path), source="AI Engineering Guide")

        # Query
        logger.info("\n=== Query 1: RAG ===")
        result = rag.query("What is RAG and how does it work?")
        logger.info(f"Answer: {result.answer[:300]}...")
        logger.info(f"Sources: {[r.chunk.id for r in result.supporting_chunks]}")

        logger.info("\n=== Query 2: Multimodal ===")
        result = rag.query("What are multimodal AI systems?")
        logger.info(f"Answer: {result.answer[:300]}...")

        logger.info("\n=== Query 3: Vector DBs ===")
        result = rag.query("What vector databases are mentioned?")
        logger.info(f"Answer: {result.answer[:300]}...")

    finally:
        rag.close()
        # Cleanup
        import shutil
        shutil.rmtree(sample_dir, ignore_errors=True)


if __name__ == "__main__":
    demo()