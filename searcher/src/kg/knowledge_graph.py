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


class KnowledgeGraphConstructor:
    def __init__(self):
        self.added = {}
        self.nodes = []
        self.edges = []

    def data_from_es(self, es_client, index_name, max_size):
        chunks = []
        response = es_client.search(
                index=index_name,
                size=max_size,
                body={"query": {"match_all": {}}})
        for hit in response['hits']['hits']:
            chunk = hit['_source']['text']
            chunk_id = hit['_id']
            chunks.append({'text': chunk, 'id': chunk_id})
        return chunks

    def chunk_to_triplets(self, oa_client, llm, chunks):
        client = instructor.from_openai(oa_client)
        all_triplets = {}
        for chunk in chunks:
            triplets = client.chat.completions.create(
                model=llm,
                messages=[{"role": "system",
                           "content": """you are an expert in
                           extracting important information from texts.
                           You only extract relevant entities and
                           relationships between them.
                           In the sentence 'John eats pizza', you
                           would extract only 'John', because 'pizza'
                           is not a relevant entity."""},
                          {"role": "user",
                           "content": f"""
                           Obtain entities and relationships between
                           them using the following text:
                           '''{chunk['text']}'''.
                           """}],
                response_model=TripletList,
            )
            all_triplets[chunk['id']] = triplets.triplets
        return all_triplets

    def process_triplets(self, triplets):
        for id, values in triplets.items():
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
            'x': round(random.uniform(0, 50), 1),
            'y': round(random.uniform(0, 50), 1),
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
