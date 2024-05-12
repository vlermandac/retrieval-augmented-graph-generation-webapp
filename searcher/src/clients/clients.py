from elasticsearch import Elasticsearch
from openai import OpenAI


class Clients:
    def __init__(self, ELASTIC_URL, ELASTIC_PASSWORD, CA_CERT, OPENAI_API_KEY):
        self.es_client = Elasticsearch(
            ELASTIC_URL,
            ca_certs=CA_CERT,
            basic_auth=("elastic", ELASTIC_PASSWORD)
        )

        self.oa_client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def open_ai(self):
        return self.oa_client

    def elastic_search(self):
        return self.es_client
