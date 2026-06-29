from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    source: str


DOCUMENT = """
RAG systems improve language model answers by retrieving external evidence.
Chunking controls the unit of retrieval and affects precision.
Hybrid search combines keyword matching with vector similarity.
Evaluation uses golden datasets, Recall@K, MRR, and groundedness checks.
"""


def chunk_text(text: str, source: str) -> list[Chunk]:
    sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]
    return [
        Chunk(chunk_id=f"{source}-{index}", text=sentence, source=source)
        for index, sentence in enumerate(sentences)
    ]


def keyword_score(query: str, chunk: Chunk) -> int:
    query_terms = set(query.lower().split())
    chunk_terms = set(chunk.text.lower().split())
    return len(query_terms & chunk_terms)


def retrieve(query: str, chunks: list[Chunk], top_k: int = 2) -> list[tuple[int, Chunk]]:
    scored = [(keyword_score(query, chunk), chunk) for chunk in chunks]
    return sorted(scored, key=lambda item: item[0], reverse=True)[:top_k]


def answer(query: str, evidence: list[tuple[int, Chunk]]) -> str:
    citations = ", ".join(chunk.chunk_id for _, chunk in evidence)
    context = " ".join(chunk.text for _, chunk in evidence)
    return f"Question: {query}\nAnswer evidence: {context}\nCitations: {citations}"


def main() -> None:
    chunks = chunk_text(DOCUMENT, source="rag-notes")
    query = "How do we evaluate RAG retrieval?"
    evidence = retrieve(query, chunks)
    print(answer(query, evidence))


if __name__ == "__main__":
    main()

