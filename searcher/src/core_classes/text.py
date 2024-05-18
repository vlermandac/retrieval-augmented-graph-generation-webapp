from pydantic import BaseModel, Field
from typing import Optional, Callable, TypeVar

T = TypeVar('T', bound='Text')


class Text(BaseModel):
    id: str
    text: str
    metadata: Optional[dict] = None
    embedding: Optional[list] = None

    def create_child(self, new_id: str, new_text: str) -> 'Text':
        return Text(id=new_id, text=new_text,
                    metadata=self.metadata.copy() if self.metadata else None)
