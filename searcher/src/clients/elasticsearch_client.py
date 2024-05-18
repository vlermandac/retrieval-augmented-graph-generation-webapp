from typing import Any, Dict, Optional, Union, List
from elasticsearch import Elasticsearch
import os
import sys

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(pwd, '../src'))
from core_classes import Text, DatabaseClient  # noqa


class ElasticsearchClient(DatabaseClient):
    def __init__(self, ELASTIC_URL: str, ELASTIC_PASSWORD: str, CA_CERT: str):
        self.client = Elasticsearch(
            ELASTIC_URL,
            ca_certs=CA_CERT,
            basic_auth=("elastic", ELASTIC_PASSWORD)
        )

    def create_index(self, name: str, settings: Optional[Dict[str, Any]] = None):
        return self.client.indices.create(index=name, body=settings or {}, ignore=400)

    def index(self, index: str, text: Text):
        return self.client.index(index=index,
                                 id=text.id,
                                 body={"text": text.text,
                                       "metadata": text.metadata,
                                       "embedding": text.embedding},
                                 ignore=400)

    def delete(self, index: str, id: Optional[str] = None):
        if id:
            return self.client.delete(index=index, id=id, ignore=400)
        return self.client.indices.delete(index=index, ignore=400)

    def search(self, index: str, id: Optional[str] = None, size: Optional[int] = 10000) -> Union[Text, List[Text]]:
        if id:
            response = self.client.get(index=index, id=id, size=size)
            return Text(id=response["_id"],
                        text=response["_source"]["text"],
                        metadata=response["_source"].get("metadata"))

        else:
            response = self.client.search(index=index,
                                          size=size,
                                          body={"query": {"match_all": {}}})

            return [
                Text(id=hit["_id"], text=hit["_source"]["text"],
                     metadata=hit["_source"].get("metadata"))
                for hit in response["hits"]["hits"]
            ]

    def semantic_search(self, index: str, vector: List[float], k: int) -> List[Text]:
        response = self.client.search(
            index=index,
            knn={
                "field": "embedding",
                "query_vector": vector,
                "k": k,
                "num_candidates": k * 4,
            },
        )
        return self.retrieval_parser(response)

    def retrieval_parser(self, response) -> List[Text]:
        output = []
        if len(response["hits"]["hits"]) == 0:
            print("Your search returned no results.")
        else:
            for hit in response["hits"]["hits"]:
                text = hit["_source"]["text"]
                id = hit["_id"]
                output.append(Text(id=id, text=text))
        return output
