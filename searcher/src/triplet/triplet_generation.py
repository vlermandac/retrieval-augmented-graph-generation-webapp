from pydantic import BaseModel, Field
from typing import List
import instructor
from core_classes import (
    Triplet, TripletListId, TripletLists, LLM, TextItem
)


class TripletList(BaseModel):
    triplets: List[Triplet] = Field(..., default_factory=list)


class TripletBuilder:
    def __init__(self, chunks: List[TextItem], llm: LLM) -> None:
        self.llm = llm
        self.client = instructor.from_openai(llm.client)
        self.all_triplets = []
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            print(f"\rProcessing chunk {i + 1}/{total_chunks}", end="")
            triplets = self.text_to_triplet(chunk.text)
            self.all_triplets.append(
                TripletListId(
                    id=chunk.id,
                    triplets=triplets.triplets
                )
            )

    def get_triplets(self) -> TripletLists:
        return TripletLists(root=self.all_triplets)

    def save_as_json(self, path: str) -> str:
        triplets = self.get_triplets()
        with open(path, 'w') as file:
            file.write(triplets.model_dump_json(indent=2))
        return triplets

    def text_to_triplet(self, text: str) -> TripletList:
        triplets = self.client.chat.completions.create(
            model=self.llm.model,
            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    You are an expert in extracting the most important
                    information from text. You extract entities
                    and relationships between them.
                    Entities can be a person, organization, or location.
                    Entities MUST NOT be actions or events.
                    You extract the triplets in the below format:
                    '''
                    {entity1, relationship, entity2}
                    '''
                    """
                },
                {
                    "role": "user",
                    "content":
                    f"""
                    Obtain entities and relationship in the format
                    (entity1, relationship, entity2) from the below text:
                    '''{text}'''.
                    """
                }
            ],
            response_model=TripletList,
            max_retries=3
        )
        return triplets
