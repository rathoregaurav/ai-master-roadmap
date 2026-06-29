def recall_at_k(expected_ids: set[str], retrieved_ids: list[str], k: int) -> float:
    if not expected_ids:
        return 0.0
    top_k = set(retrieved_ids[:k])
    return len(expected_ids & top_k) / len(expected_ids)


def reciprocal_rank(expected_ids: set[str], retrieved_ids: list[str]) -> float:
    for index, retrieved_id in enumerate(retrieved_ids, start=1):
        if retrieved_id in expected_ids:
            return 1.0 / index
    return 0.0


def mean_reciprocal_rank(cases: list[tuple[set[str], list[str]]]) -> float:
    if not cases:
        return 0.0
    return sum(reciprocal_rank(expected, retrieved) for expected, retrieved in cases) / len(cases)


if __name__ == "__main__":
    expected = {"chunk-2"}
    retrieved = ["chunk-9", "chunk-2", "chunk-1"]
    print("Recall@2:", recall_at_k(expected, retrieved, 2))
    print("RR:", reciprocal_rank(expected, retrieved))

