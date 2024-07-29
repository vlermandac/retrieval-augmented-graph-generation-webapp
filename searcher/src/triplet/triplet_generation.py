from pydantic import BaseModel, Field
from typing import List, Dict
import instructor
import os
import json
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

    def save_as_json(self, path: str) -> TripletLists:
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
                    {entidad1, relacion, entidad2}
                    '''
                    """
                },
                {
                    "role": "user",
                    "content":
                    f"""
                    Obtén entidades y relaciones en el formato
                    (entidad1, relacion, entidad2) desde el siguiente texto:
                    '''{text}'''.
                    """
                }
            ],
            response_model=TripletList,
            max_retries=2
        )
        return triplets

    def entities_freq_to_json(self, path: str) -> str:
        if (self.all_triplets is None) or (len(self.all_triplets) == 0):
            return "No triplets found."
        entities = {}
        for triplet in self.all_triplets:
            for t in triplet.triplets:
                entities[t.entity1] = entities.get(t.entity1, 0) + 1
                entities[t.entity2] = entities.get(t.entity2, 0) + 1
        entities_file = os.path.join(path, 'entities.json')
        with open(entities_file, 'w') as file:
            json.dump(entities, file, indent=2)
        return "Entities frequency saved as JSON."
