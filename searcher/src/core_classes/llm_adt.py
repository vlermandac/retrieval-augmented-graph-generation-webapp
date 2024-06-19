from abc import ABC, abstractmethod


class LLM(ABC):
    model: str

    @abstractmethod
    def inference(self, **kwargs) -> str:
        pass
