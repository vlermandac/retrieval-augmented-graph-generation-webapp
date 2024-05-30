import instructor
from typing import List
from pydantic import BaseModel, RootModel, Field


class Triplet(BaseModel):
    entity1: str
    relation: str
    entity2: str


class TripletList(BaseModel):
    triplets: List[Triplet] = Field(..., default_factory=list)


class TripletListId(BaseModel):
    id: int
    triplets: TripletList


class TripletLists(RootModel):
    root: List[TripletListId] = Field(..., default_factory=list)


class TripletBuilder:
    def chunks_to_triplets(self, oa_client, llm, chunks) -> TripletLists:
        client = instructor.from_openai(oa_client)
        all_triplets = []
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            print(f"\rProcessing chunk {i + 1}/{total_chunks}", end="")
            triplets = self.text_to_triplet(client, llm, chunk.text)
            all_triplets.append(TripletListId(id=chunk.id, triplets=triplets))
        return TripletLists(root=all_triplets)

    def text_to_triplet(self, client, llm, text) -> TripletList:
        triplets = client.chat.completions.create(
            model=llm,
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
