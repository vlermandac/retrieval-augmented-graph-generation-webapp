from abc import ABC, abstractmethod
from typing import List


class EmbeddingModel(ABC):
    model: str
    dims: int

    @abstractmethod
    def create(self, input: str) -> List[float]:
        pass
