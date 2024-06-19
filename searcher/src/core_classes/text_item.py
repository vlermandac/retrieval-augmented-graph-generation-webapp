from pydantic import BaseModel
from typing import Optional, TypeVar, List, Dict

T = TypeVar('T', bound='TextItem')


class TextItem(BaseModel, validate_assignment=True):
    id: str
    text: str
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict] = None

    def create_child(self, new_id: str, new_text: str) -> 'TextItem':
        return TextItem(
            id=new_id, text=new_text,
            metadata=self.metadata.copy() if self.metadata else None)
