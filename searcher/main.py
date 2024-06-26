import logging
from fastapi import UploadFile
from typing import List, Tuple
import sys
import os

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, './src'))

from rag import RAG  # noqa: E402
from config import ConfigVariables  # noqa: E402
from triplet import TripletBuilder  # noqa: E402
from core_classes import (
    EditableOptions, TextItem, TripletLists
)  # noqa: E402
from utils import doc_name_format  # noqa: E402
from data_ingestion import (
    Pipeline, read_pdf, chunk, embed, index, local_storage
)  # noqa: E402
from clients import (
    OAIEmbeddingClient, OAIChatClient, ElasticsearchClient
)  # noqa: E402

logger = logging.getLogger(__name__)


class Main:
    def __init__(self):
        self.c_vars = ConfigVariables(root='./')
        self.data_path = list(self.c_vars('data_path').values())[0]
        os.makedirs(self.data_path, exist_ok=True)
        self.db = ElasticsearchClient(
            **self.c_vars.env_vars(
                'ELASTIC_URL',
                'ELASTIC_PASSWORD',
                'CA_CERT'
            )
        )
        self.llm = OAIChatClient(
            **self.c_vars('chat_model'),
            **self.c_vars.env_vars("OPENAI_API_KEY")
        )
        self.embedding = OAIEmbeddingClient(
            **self.c_vars(
                'embedding_model',
                'embedding_dimension'
            ),
            **self.c_vars.env_vars("OPENAI_API_KEY")
        )

    def update_config(self, **kwargs) -> str:
        new_config = EditableOptions(**kwargs)
        self.c_vars.update_config(new_config.config_format())
        return "Config updated."

    def get_config(self) -> dict:
        return self.c_vars(
            'index_name',
            'chat_model',
            'embedding_model',
            'embedding_dimension',
            'chunk_size',
            'chunk_overlap',
            'top_k'
        )

    def list_indices(self) -> List[str]:
        return os.listdir(self.data_path)

    def ingest_data(self, file: UploadFile) -> str:
        file_path = local_storage.create_storage_path(
            filename=file.filename,
            from_dir=self.data_path
        )
        local_storage.save_file(file, file_path)
        print(f"file path: {file_path}")
        (Pipeline() | read_pdf(file_path)
                    | chunk(**self.c_vars('chunk_size', 'chunk_overlap'))
                    | embed(self.embedding)
                    | index(self.db))
        return doc_name_format(file_path).title

    def generate_triplets(self, index: str) -> TripletLists:
        file_path = os.path.join(self.data_path, index, 'triplets.json')
        triplets = TripletBuilder(
            chunks=self.db.search(index),
            llm=self.llm
        )
        item = TextItem(id=index, text='', metadata=triplets.get_entities())
        self.db.index(index, item)
        return triplets.save_as_json(file_path)

    def query_rag(self, query: str) -> Tuple[str, List[str]]:
        rag = RAG(
            self.db, self.embedding, self.llm,
            **self.c_vars('index_name', 'top_k')
        )
        response_text, retrieval_ids = rag(query=query)
        return response_text, retrieval_ids

    def delete_index(self, index: str) -> str:
        self.db.delete(index)
        index_path = os.path.join(self.data_path, index)
        local_storage.delete_dir(index_path)
        return f"Index {index} deleted."


if __name__ == "__main__":
    main = Main()
    # parse_args = Arguments() | "--load_file" | "--RAG" | "--triplets"
    # selected_arg = parse_args()
