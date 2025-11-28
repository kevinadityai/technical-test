import random
from typing import List


class EmbeddingService:
    def __init__(self, vector_size: int = 128):
        self.vector_size = vector_size

    def embed(self, text: str) -> List[float]:
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.vector_size)]
