from .preprocess import pdf_to_text, chunking
from .index import index_items
from .embedding import add_embedding
from core_classes import EmbeddingModel, Database, TextItem
from pydantic import BaseModel
from typing import List, Callable, Optional


class Pipeline(BaseModel):
    document: Optional[TextItem] = None
    chunks: Optional[List[TextItem]] = None

    def read_pdf(self, file_path: str) -> 'Pipeline':
        self.document = pdf_to_text(file_path)
        self.chunks = [self.document]
        return self

    def chunk(self, chunk_size: int, chunk_overlap: int) -> 'Pipeline':
        self.chunks = chunking(self.document, chunk_size, chunk_overlap)
        return self

    def embed(self, embedding: EmbeddingModel) -> 'Pipeline':
        add_embedding(self.chunks, embedding)
        return self

    def index(self, db: Database) -> 'Pipeline':
        index = self.document.metadata['title']
        index_items(db, index, self.chunks)
        return self

    def __or__(self, other: Callable[['Pipeline'], 'Pipeline']) -> 'Pipeline':
        return other(self)


def step(func: Callable[..., 'Pipeline'], *args, **kwargs) -> Callable[[Pipeline], Pipeline]:
    def wrapper(pipeline: Pipeline) -> Pipeline:
        return func(pipeline, *args, **kwargs)
    return wrapper


def read_pdf(file_path: str) -> Callable[[Pipeline], Pipeline]:
    return step(Pipeline.read_pdf, file_path)


def chunk(chunk_size: int, chunk_overlap: int) -> Callable[[Pipeline], Pipeline]:
    return step(Pipeline.chunk, chunk_size, chunk_overlap)


def embed(embedding: EmbeddingModel) -> Callable[[Pipeline], Pipeline]:
    return step(Pipeline.embed, embedding)


def index(db: Database) -> Callable[[Pipeline], Pipeline]:
    return step(Pipeline.index, db)
