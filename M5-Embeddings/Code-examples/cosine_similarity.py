import math


def dot_product(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("vectors must have the same length")
    return sum(x * y for x, y in zip(a, b))


def magnitude(vector: list[float]) -> float:
    return math.sqrt(sum(value * value for value in vector))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    denominator = magnitude(a) * magnitude(b)
    if denominator == 0:
        return 0.0
    return dot_product(a, b) / denominator


if __name__ == "__main__":
    query = [1.0, 0.2, 0.1]
    document_a = [0.9, 0.1, 0.2]
    document_b = [0.1, 0.8, 0.7]

    print("A:", round(cosine_similarity(query, document_a), 3))
    print("B:", round(cosine_similarity(query, document_b), 3))
