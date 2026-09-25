import math
import re
from typing import List, Dict, Any


def tokenize(text: str) -> List[str]:
    """Simple alphanumeric tokenizer for lightweight vector similarity computation."""
    return re.findall(r"\w+", text.lower())


def compute_tf(tokens: List[str]) -> Dict[str, float]:
    tf: Dict[str, float] = {}
    total = len(tokens)
    if total == 0:
        return tf
    for token in tokens:
        tf[token] = tf.get(token, 0.0) + 1.0
    for token in tf:
        tf[token] /= total
    return tf


def cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    intersection = set(vec1.keys()) & set(vec2.keys())
    dot_product = sum([vec1[x] * vec2[x] for x in intersection])

    mag1 = math.sqrt(sum([val**2 for val in vec1.values()]))
    mag2 = math.sqrt(sum([val**2 for val in vec2.values()]))

    if not mag1 or not mag2:
        return 0.0

    return dot_product / (mag1 * mag2)
