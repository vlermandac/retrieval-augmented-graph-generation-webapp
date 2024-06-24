from typing import List, Optional
from pydantic import BaseModel, Field, RootModel, field_validator


class Triplet(BaseModel):
    entity1: Optional[str] = Field("N/A", title="Entity 1")
    relation: Optional[str] = Field("N/A", title="Relation")
    entity2: Optional[str] = Field("N/A", title="Entity 2")

    @field_validator('*', mode='after')
    @classmethod
    def replace_empty(cls, v):
        if (v is None or v == "" or v == "\n"):
            v = "N/A"
            return v
        return v.replace("\n", " ").replace("\t", " ").lower()


class TripletListId(BaseModel):
    id: int
    triplets: List[Triplet] = Field(..., default_factory=list)


class TripletLists(RootModel):
    root: List[TripletListId] = Field(..., default_factory=list)
