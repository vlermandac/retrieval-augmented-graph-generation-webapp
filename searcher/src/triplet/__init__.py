from .triplet_generation import TripletBuilder
from .disambiguation import process_triplets


def get_triplets(chunks: list[str], llm: str):
    tb = TripletBuilder()
    tri = tb.chunks_to_triplets(chunks=chunks, llm=llm)
    tri = process_triplets(tri)
    return tri.model_dump_json(indent=2)
