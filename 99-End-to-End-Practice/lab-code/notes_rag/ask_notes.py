from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source: str
    text: str


def load_markdown_files(root: Path) -> list[Path]:
    ignored_parts = {".git", ".pycache", "__pycache__"}
    files = []
    for path in root.rglob("*.md"):
        if any(part in ignored_parts for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def chunk_text(source: Path, text: str, max_words: int = 120) -> list[Chunk]:
    words = text.split()
    chunks = []
    for index, start in enumerate(range(0, len(words), max_words)):
        chunk_words = words[start : start + max_words]
        chunks.append(
            Chunk(
                chunk_id=f"{source.stem}-{index}",
                source=str(source.relative_to(REPO_ROOT)),
                text=" ".join(chunk_words),
            )
        )
    return chunks


def tokenize(text: str) -> set[str]:
    cleaned = text.lower()
    for char in ",.:;!?()[]{}#`*_-/":
        cleaned = cleaned.replace(char, " ")
    return {word for word in cleaned.split() if len(word) > 2}


def score(query: str, chunk: Chunk) -> int:
    return len(tokenize(query) & tokenize(chunk.text))


def retrieve(query: str, chunks: list[Chunk], top_k: int = 4) -> list[tuple[int, Chunk]]:
    scored = [(score(query, chunk), chunk) for chunk in chunks]
    useful = [item for item in scored if item[0] > 0]
    return sorted(useful, key=lambda item: item[0], reverse=True)[:top_k]


def answer(query: str, results: list[tuple[int, Chunk]]) -> str:
    if not results:
        return "I could not find matching notes yet. Add more notes or try a clearer query."

    lines = [f"Question: {query}", "", "Best matching notes:"]
    for rank, (match_score, chunk) in enumerate(results, start=1):
        preview = chunk.text[:350].strip()
        lines.append(f"{rank}. score={match_score} source={chunk.source} chunk={chunk.chunk_id}")
        lines.append(f"   {preview}")
    return "\n".join(lines)


def main() -> None:
    query = " ".join(sys.argv[1:]).strip()
    if not query:
        query = "What is RAG?"

    chunks = []
    for path in load_markdown_files(REPO_ROOT):
        chunks.extend(chunk_text(path, path.read_text(encoding="utf-8")))

    print(answer(query, retrieve(query, chunks)))


if __name__ == "__main__":
    main()

