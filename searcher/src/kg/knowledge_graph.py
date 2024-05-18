import instructor
from typing import List, Any
from pydantic import BaseModel, Field
import random


class Attributes(BaseModel):
    label: str
    size: int
    x: float | None
    y: float | None
    forceLabel: bool | None
    chunk_id: str | None


class Node(BaseModel):
    key: str
    attributes: Attributes


class Edge(BaseModel):
    source: str
    target: str
    attributes: Attributes


class Triplet(BaseModel):
    entity1: str
    relation: str
    entity2: str


class TripletList(BaseModel):
    triplets: List[Triplet] = Field(..., default_factory=list)


class KnowledgeGraph(BaseModel):
    attributes: Any
    nodes: List[Node]
    edges: List[Edge]
    options: Any


class KnowledgeGraphBuilder:
    def __init__(self):
        self.added = {}
        self.nodes = []
        self.edges = []

    def chunk_to_triplets(self, oa_client, llm, chunks):
        client = instructor.from_openai(oa_client)
        all_triplets = {}
        total_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            print(f"\rProcessing chunk {i + 1}/{total_chunks}", end="")
            triplets = client.chat.completions.create(
                model=llm,
                messages=[{"role": "system",
                           "content": """
                           You are an expert in extracting the most important information from text.
                           You only extract entities and relationships between them in a triplet 
                           format, like {entity1, relationship, entity2}.
                           """},
                          {"role": "system",
                           "content": """
                            Here are examples of good triplets:
                            "John is an engineer that works at Google from 9 to 5": {John, works at, Google}
                            "John is the guitarist of the band The Beatles": {John, guitarist of, The Beatles},
                            {John, plays, guitar}, {John, member of, The Beatles}, {John, is, musician}.
                           """},
                          {"role": "system",
                           "content": """
                            Examples of bad triplets that you should avoid:
                            {John, is, a person}: The relationship is not relevant,
                            and 'a person' is not a specific entity.
                            {Beautiful red-haired Mary, is married to, John}: Mary should not
                            be described in such detail, and instead 'Mary' should be used.
                            Also, the relationship instead of 'is married to' should be 'married to'.
                            {John, hates, traffics lights}: The relationship could be relevant, but the
                            entity 'traffic lights' is not relevant.
                           """},
                          {"role": "user",
                           "content": f"""
                           Obtain entities and relationships between
                           them using the following text:
                           '''{chunk.text}'''.
                           """}],
                response_model=TripletList,
            )
            all_triplets[chunk.id] = triplets.triplets
        return all_triplets

    def process_triplets(self, triplets):
        triplets_size = len(triplets)
        i = 0
        for id, values in triplets.items():
            i += 1
            print(f"\rProcessing chunk {i}/{triplets_size}", end="")
            for triplet in values:
                src = triplet.entity1
                trg = triplet.entity2
                rl = triplet.relation
                att_map = {
                    'label': rl,
                    'size': 3,
                    'x': None,
                    'y': None,
                    'forceLabel': True,
                    'chunk_id': id
                }
                atts = Attributes(**att_map)
                edge = Edge(source=src, target=trg, attributes=atts)
                self.edges.append(edge)
                self.add_node(src)
                self.add_node(trg)

    def add_node(self, key):
        if key in self.added:
            return
        self.added[key] = True
        att_map = {
            'label': key,
            'size': 20,
            'x': round(random.uniform(0, 500), 2),
            'y': round(random.uniform(0, 500), 2),
            'forceLabel': None,
            'chunk_id': None
        }
        atts = Attributes(**att_map)
        node = Node(key=key, attributes=atts)
        self.nodes.append(node)

    def serialize(self):
        kg_map = {
            'attributes': {},
            'nodes': self.nodes,
            'edges': self.edges,
            'options': {"multi": True}
        }
        return KnowledgeGraph(**kg_map).model_dump_json(indent=2)
