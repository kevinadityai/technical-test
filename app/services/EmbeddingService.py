import random


def fake_embed(text: str):
    random.seed(abs(hash(text)) % 10000)
    return [random.random() for _ in range(128)]
