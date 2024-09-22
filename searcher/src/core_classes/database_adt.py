from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
from .text_item import TextItem


class Database(ABC):
    data_mapping: Optional[Dict[str, Any]] = None

    @abstractmethod
    def create_index(self, name: str, dims: int):
        pass

    @abstractmethod
    def index(self, index: str, item: TextItem):
        pass

    @abstractmethod
    def search(self, index: str, id: Optional[str] = None) -> Union[TextItem, List[TextItem]]:
        pass

    @abstractmethod
    def semantic_search(self, index: str, vector: List[float], k: int) -> List[TextItem]:
        pass

    @abstractmethod
    def delete(self, index: str, id: Optional[str] = None):
        pass
