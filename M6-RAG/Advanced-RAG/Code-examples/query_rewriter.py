def rewrite_query(query: str) -> list[str]:
    base = query.strip()
    return [
        base,
        f"definition and explanation of {base}",
        f"implementation details and examples for {base}",
    ]


def compress_context(chunks: list[str], required_terms: list[str]) -> list[str]:
    compressed = []
    lowered_terms = [term.lower() for term in required_terms]
    for chunk in chunks:
        lower_chunk = chunk.lower()
        if any(term in lower_chunk for term in lowered_terms):
            compressed.append(chunk)
    return compressed


if __name__ == "__main__":
    print(rewrite_query("hybrid search in RAG"))
    print(compress_context(["RAG uses retrieval.", "FastAPI streams data."], ["retrieval"]))

