from core_classes import TextItem, EmbeddingModel
from typing import List


def add_embedding(texts: List[TextItem], embedding: EmbeddingModel) -> None:
    for ti in texts:
        ti.embedding = embedding.create(input=ti.text)
        print(f"\rEmbedding {ti.id}...{
            round((int(ti.id)+1)/len(texts)*100, 2)}%", end="")
