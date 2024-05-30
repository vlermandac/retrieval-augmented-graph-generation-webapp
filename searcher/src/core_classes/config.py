from pydantic import BaseModel


class PreprocessConfig(BaseModel):
    chunk_size: int
    chunk_overlap: int


class LLMConfig(BaseModel):
    chat_model: str
    embedding_model: str
    embedding_dimension: int


class RAGConfig(BaseModel):
    index_name: str
    top_k: int


class Config(BaseModel):
    preprocess: PreprocessConfig
    llm: LLMConfig
    rag: RAGConfig
