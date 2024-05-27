import os
import sys
pwd = os.path.dirname(os.path.abspath(__file__))
os.chdir(pwd)
sys.path.append(os.path.join(pwd, './src'))

from utils import Arguments  # noqa: E402
from config import ConfigVariables  # noqa: E402
from clients import Clients  # noqa: E402
from rag import RAG  # noqa: E402
import data_loading  # noqa: E402
from triplet import TripletBuilder  # noqa: E402


class Main:
    def __init__(self):
        self.cfg_vars = ConfigVariables(root='./')
        self.clients = Clients(**self.cfg_vars.env_vars(
                        "ELASTIC_PASSWORD", "ELASTIC_URL",
                        "CA_CERT", "OPENAI_API_KEY"))

    def run(self, flag: str, query: str = None):

        if flag == "--load_data":
            data_loading.run(self.clients, **self.cfg_vars(
                            'unprocessed_files', 'chunk_size',
                            'overlap', 'embedding_model', 'dims'))
            f1 = list(self.cfg_vars('unprocessed_files').values())[0]
            f2 = list(self.cfg_vars('processed_files').values())[0]
            mv_cmd = f"mv {f1}/*.pdf {f2}"
            os.system(mv_cmd)

        if flag == "--RAG":
            rag = RAG(self.clients,
                      **self.cfg_vars('index', 'embedding_model',
                                      'dims', 'llm', 'k'))
            return rag(query=query)

        if flag == "--triplets":
            tb = TripletBuilder()
            v1 = list(self.cfg_vars('index').values())[0]
            v2 = list(self.cfg_vars('llm').values())[0]
            chunks = self.clients.elastic_search().search(v1)
            triplets = tb.chunk_to_triplets(self.clients.open_ai(), v2, chunks)
            triplets = triplets.model_dump_json(indent=2)
            with open('../data/triplets.json', 'w') as f:
                f.write(triplets)
            return triplets


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
