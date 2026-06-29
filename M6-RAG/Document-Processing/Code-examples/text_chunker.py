from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    start_word: int
    end_word: int


def chunk_text(text: str, chunk_size: int = 120, overlap: int = 20) -> list[Chunk]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks: list[Chunk] = []
    start = 0
    index = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(
            Chunk(
                chunk_id=f"chunk-{index}",
                text=" ".join(words[start:end]),
                start_word=start,
                end_word=end,
            )
        )
        if end == len(words):
            break
        start = end - overlap
        index += 1
    return chunks


if __name__ == "__main__":
    sample = " ".join(f"word{i}" for i in range(260))
    for chunk in chunk_text(sample, chunk_size=80, overlap=10):
        print(chunk.chunk_id, chunk.start_word, chunk.end_word)

