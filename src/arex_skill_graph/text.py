from __future__ import annotations

from collections import Counter
from hashlib import blake2b
import math
import re
from typing import Iterable


TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_./:-]*|[\u4e00-\u9fff]+")

STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "this",
        "to",
        "with",
        "fix",
        "feat",
        "chore",
    }
)


def tokenize(text: str) -> list[str]:
    return [
        token
        for raw in TOKEN_RE.findall(text.lower())
        if (token := raw.strip("._/-:")) and token not in STOPWORDS and len(token) > 1
    ]


def hash_embedding(text: str, dimensions: int = 256) -> list[float]:
    """Dependency-free signed feature-hashing embedding.

    It is intentionally deterministic and cheap. It gives the pilot a vector
    retrieval channel without an external model call. Production can replace
    it with a code/text embedding model and HNSW without changing the store or
    retrieval API.
    """

    vector = [0.0] * dimensions
    counts = Counter(tokenize(text))
    for token, count in counts.items():
        digest = blake2b(token.encode("utf-8"), digest_size=16).digest()
        index = int.from_bytes(digest[:8], "little") % dimensions
        sign = -1.0 if digest[8] & 1 else 1.0
        vector[index] += sign * (1.0 + math.log(count))
    return normalize(vector)


def normalize(vector: Iterable[float]) -> list[float]:
    values = [float(value) for value in vector]
    norm = math.sqrt(sum(value * value for value in values))
    if norm == 0:
        return values
    return [value / norm for value in values]


def cosine(left: Iterable[float], right: Iterable[float]) -> float:
    left_values = list(left)
    right_values = list(right)
    if len(left_values) != len(right_values):
        raise ValueError("vectors must have the same dimensions")
    return sum(a * b for a, b in zip(left_values, right_values))

