from typing import List
from pydantic import BaseModel, Field, RootModel


class Triplet(BaseModel):
    entity1: str
    relation: str
    entity2: str


class TripletListId(BaseModel):
    id: int
    triplets: List[Triplet] = Field(..., default_factory=list)


class TripletLists(RootModel):
    root: List[TripletListId] = Field(..., default_factory=list)
