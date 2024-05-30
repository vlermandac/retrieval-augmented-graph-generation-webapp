import os
import sys
import shutil
from fastapi import UploadFile
from typing import Union, Literal, Tuple, List

pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, './src'))

from config import ConfigVariables  # noqa: E402
from core_classes import PreprocessConfig, LLMConfig, RAGConfig, Config  # noqa: E402
from utils import Arguments  # noqa: E402
from clients import Clients  # noqa: E402
from rag import RAG  # noqa: E402
import data_loading  # noqa: E402
from triplet import get_triplets  # noqa: E402


class Main:
    def __init__(self):
        self.cfg_vars = ConfigVariables(root='./')
        self.clients = Clients(
            **self.cfg_vars.env_vars(
                "ELASTIC_PASSWORD",
                "ELASTIC_URL",
                "CA_CERT",
                "OPENAI_API_KEY"
            )
        )

    def update_config(
        self, index_name: str,
        chat_model: Literal["gpt-4o", "gpt-3.5-turbo"],
        chunk_size: int, chunk_overlap: int,
        embedding_model: str, top_k: int
    ) -> str:

        preprocess = PreprocessConfig(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        llm = LLMConfig(
            embedding_model=embedding_model,
            embedding_dimension=200,
            chat_model=chat_model
        )

        rag = RAGConfig(
            index_name=index_name,
            top_k=top_k
        )

        self.cfg_vars.update_config(
            Config(preprocess=preprocess, llm=llm, rag=rag)
        )
        return "Config updated."

    def get_config(self) -> dict:
        return self.cfg_vars(
            'index_name',
            'chat_model',
            'embedding_model',
            'chunk_size',
            'chunk_overlap',
            'top_k'
        )

    def list_files(self) -> List[str]:
        f1 = list(self.cfg_vars('processed_files').values())[0]
        return [f.split('.')[0].split('-')[1].lower() + '-chunk' for f in os.listdir(f1)]

    def run(
        self, flag: str,
        request: Union[str, UploadFile] = None
    ) -> Union[str, Tuple[str, List[int]]]:

        if flag == "--load_data":
            f1 = list(self.cfg_vars('unprocessed_files').values())[0]
            f2 = list(self.cfg_vars('processed_files').values())[0]
            os.makedirs(f1, exist_ok=True)
            os.makedirs(f2, exist_ok=True)

            file_path = os.path.join(f1, request.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(request.file, buffer)

            data_loading.run(
                self.clients, **self.cfg_vars(
                    'unprocessed_files',
                    'chunk_size',
                    'chunk_overlap',
                    'embedding_model',
                    'embedding_dimension'
                )
            )
            mv_cmd = f"mv {f1}/*.pdf {f2}"
            os.system(mv_cmd)
            return f"Document {request.filename} loaded."

        if flag == "--RAG":
            rag = RAG(
                self.clients, **self.cfg_vars(
                    'index_name',
                    'embedding_model',
                    'embedding_dimension',
                    'chat_model',
                    'top_k'
                )
            )
            return rag(query=request)

        if flag == "--triplets":
            v1 = list(self.cfg_vars('index_name').values())[0]
            v2 = list(self.cfg_vars('chat_model').values())[0]

            chunks = self.clients.elastic_search().search(v1)
            triplets = get_triplets(chunks, v2)
            file_path = "../data/triplets.json"

            with open(file_path, 'w') as file:
                file.write(triplets)
            return f"Triplets generated at {file_path}"


if __name__ == "__main__":
    parse_args = Arguments() | "--load_data" | "--RAG" | "--triplets"
    selected_arg = parse_args()
    main = Main()

    if selected_arg.load_data is not None:
        main.run("--load_data")

    if selected_arg.RAG is not None:
        response = main.run("--RAG", query=selected_arg.RAG[0])
        print(response)

    if selected_arg.KG is not None:
        main.run("--triplets")
