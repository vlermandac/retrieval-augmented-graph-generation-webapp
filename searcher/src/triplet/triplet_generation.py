import instructor
from typing import List
from pydantic import BaseModel, RootModel, Field
from nltk.metrics.distance import edit_distance


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
    def chunk_to_triplets(self, oa_client, llm, chunks):
        client = instructor.from_openai(oa_client)
        all_triplets = []
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            print(f"\rProcessing chunk {i + 1}/{total_chunks}", end="")
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
                        '''{chunk.text}'''.
                        """
                    }
                ],
                response_model=TripletList,
                max_retries=3
            )
            revised_triplets = self.revise_triplets(client, triplets, llm)
            merged_triplets = self.merge_entities(revised_triplets)
            all_triplets.append(TripletListId(id=chunk.id, triplets=merged_triplets))
        return TripletLists(root=all_triplets)

    def revise_triplets(self, client, triplets: TripletList, llm: str):
        revised_triplets = client.chat.completions.create(
            model=llm,
            messages=[
                {
                    "role": "system",
                    "content":
                    """
                    You are an expert in revising the extracted triplets,
                    defined as an structured format of {entity1, relationship, entity2}.
                    Entities must be a person, organization, or location.

                    You revise the triplets and do the following:
                    1. Reduce the relationship name to few words as possible.
                        Example: {Michael, is a friend since childhood of, John} -> {Michael, friend of, John}
                    2. Merge 2 or more triplets into a single triplet combining their information.
                        Remove the triplets used to create the new triplet.
                        Example: {Mary, likes, John} and {Mary, kisses, John} -> {Mary, loves, John}
                    """
                },
                {
                    "role": "user",
                    "content":
                    f"""
                    Revise the triplets extracted from the text and keep them
                    in the format (entity1, relationship, entity2).
                    triplets: {triplets}
                    """
                }
            ],
            response_model=TripletList,
            max_retries=3
        )
        return revised_triplets

    def merge_entities(self, triplet_list: TripletList, threshold: int = 90):
        triplets = triplet_list.triplets
        entity_map = {}

        for triplet in triplets:
            entity_map.setdefault(triplet.entity1, triplet.entity1)
            entity_map.setdefault(triplet.entity2, triplet.entity2)

        entities = list(entity_map.keys())

        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                max_len = max(len(entities[i]), len(entities[j]))
                if max_len == 0:
                    continue
                edit_dist = edit_distance(entities[i], entities[j])
                similarity_score = (1 - (edit_dist / max_len)) * 100
                if similarity_score >= threshold:
                    entity_map[entities[j]] = entity_map[entities[i]]

        merged_triplets = []
        for triplet in triplets:
            merged_triplets.append(Triplet(
                entity1=entity_map[triplet.entity1],
                relation=triplet.relation,
                entity2=entity_map[triplet.entity2]
            ))

        return TripletList(triplets=merged_triplets)
