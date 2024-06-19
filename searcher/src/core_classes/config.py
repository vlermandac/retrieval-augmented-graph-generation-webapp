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


class EditableOptions(BaseModel):
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    embedding_dimension: int
    chat_model: str
    index_name: str
    top_k: int

    def config_format(self) -> Config:
        return Config(
            preprocess=PreprocessConfig(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            ),
            llm=LLMConfig(
                chat_model=self.chat_model,
                embedding_model=self.embedding_model,
                embedding_dimension=self.embedding_dimension
            ),
            rag=RAGConfig(
                index_name=self.index_name,
                top_k=self.top_k
            )
        )
