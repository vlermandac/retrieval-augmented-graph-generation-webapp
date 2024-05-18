from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
from pydantic import BaseModel
from .text import Text


class DatabaseClient(ABC):
    @abstractmethod
    def create_index(self, name: str, settings: Optional[Dict[str, Any]] = None):
        pass

    @abstractmethod
    def index(self, index: str, text: Text):
        pass

    @abstractmethod
    def search(self, index: str, id: Optional[str] = None) -> Union[Text, List[Text]]:
        pass

    @abstractmethod
    def semantic_search(self, index_name: str, text: str) -> None:
        pass

    @abstractmethod
    def delete(self, index: str, id: Optional[str] = None):
        pass
