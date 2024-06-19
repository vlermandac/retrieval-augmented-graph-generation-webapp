from core_classes import EmbeddingModel
from typing import List
from openai import OpenAI


class OAIEmbeddingClient(EmbeddingModel):
    model: str
    dims: int
    client: OpenAI

    def __init__(self, embedding_model: str, embedding_dimension: int, OPENAI_API_KEY: str):
        self.model = embedding_model
        self.dims = embedding_dimension
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def create(self, input: str) -> List[float]:
        vector_repr = self.client.embeddings.create(
            input=input,
            model=self.model,
            dimensions=self.dims
        )
        return vector_repr.data[0].embedding
