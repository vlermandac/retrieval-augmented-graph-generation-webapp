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


class Main:
    def __init__(self):
        self.cfg_vars = ConfigVariables(root='./')
        self.clients = Clients(**self.cfg_vars.env_vars(
                        "ELASTIC_PASSWORD", "ELASTIC_URL",
                        "CA_CERT", "OPENAI_API_KEY"))

    def run(self, flag: str, query: str = None):
        if flag == "--process_data":
            data_loading.run(self.clients, **self.cfg_vars(
                            'processed_files', 'chunk_size',
                            'overlap', 'embedding_model', 'dims'))
            # mv_cmd = \
            #     f"""
            #     mv {self.cfg_vars('unprocessed_files')}/*.pdf
            #     {self.cfg_vars('processed_files')}
            #     """
            # os.system(mv_cmd)

        if flag == "--RAG":
            self.rag = RAG(self.clients, 'goodfellas-chunk',
                           **self.cfg_vars('embedding_model', 'dims', 'llm', 'k'))
            return self.rag(query=query)

        if flag == "--KG":
            return self.rag.get_result_ids()

        if flag == "--setup":
            return "Config setup complete"


if __name__ == "__main__":
    # note: arreglar el uso como CLI
    # parse_args = Arguments() | "--process_data" | "--RAG" | "--KG" | "--setup"
    # selected_arg = parse_args()
    selected_arg = sys.argv[1]
    main = Main()
    print(main.run(selected_arg))
