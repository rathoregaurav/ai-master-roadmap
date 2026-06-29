from collections import Counter

from cosine_similarity import cosine_similarity


DOCUMENTS = [
    "FastAPI streams AI responses with server sent events.",
    "Embeddings represent semantic meaning as numeric vectors.",
    "RAG systems retrieve evidence before generating answers.",
]


def tokenize(text: str) -> list[str]:
    return text.lower().replace(".", "").split()


def vocabulary(texts: list[str]) -> list[str]:
    words = set()
    for text in texts:
        words.update(tokenize(text))
    return sorted(words)


def bag_of_words(text: str, vocab: list[str]) -> list[float]:
    counts = Counter(tokenize(text))
    return [float(counts[word]) for word in vocab]


def search(query: str, documents: list[str], top_k: int = 2) -> list[tuple[float, str]]:
    vocab = vocabulary([query, *documents])
    query_vector = bag_of_words(query, vocab)
    scored = []
    for document in documents:
        doc_vector = bag_of_words(document, vocab)
        scored.append((cosine_similarity(query_vector, doc_vector), document))
    return sorted(scored, reverse=True)[:top_k]


if __name__ == "__main__":
    for score, document in search("How do RAG apps find evidence?", DOCUMENTS):
        print(round(score, 3), document)

