from typing import Optional, Union, List
from elasticsearch import Elasticsearch
from core_classes import TextItem, Database


class ElasticsearchClient(Database):
    vector_field: str = "embedding"

    def __init__(self, ELASTIC_URL: str, ELASTIC_PASSWORD: str, CA_CERT: str):
        self.client = Elasticsearch(
            ELASTIC_URL,
            ca_certs=CA_CERT,
            basic_auth=("elastic", ELASTIC_PASSWORD)
        )

    def create_index(self, name: str, dims: int):
        """

        To index an item with an embbeding, the index must be created
        explicitly with 'dense_vector' type.

        """
        return self.client.indices.create(
            index=name,
            body={
                "mappings": {
                    "properties": {
                        "text": {"type": "text"},
                        "metadata": {"type": "object"},
                        self.vector_field: {
                            "type": "dense_vector",
                            "dims": dims
                        }
                    }
                }
            },
            ignore=400
        )

    def index(self, index: str, item: TextItem):
        """
        Unexpectly important to set refresh=True to make the
        indexed item available for search immediately.
        """
        return self.client.index(
            index=index,
            id=item.id,
            body={
                "text": item.text,
                "metadata": item.metadata,
                self.vector_field: item.embedding
            },
            refresh=True
        )

    def delete(self, index: str, id: Optional[str] = None):
        if (id is not None):
            return self.client.delete(index=index, id=id, refresh=True)
        return self.client.indices.delete(
            index=index,
            ignore_unavailable=True
        )

    def search(
        self, index: str,
        id: Optional[str] = None
    ) -> Union[None, TextItem, List[TextItem]]:

        if not self.client.indices.exists(index=index):
            return None
        if id is not None:
            response = self.client.get(index=index, id=id, ignore=404)
            if response["found"] is False:
                return None
            return TextItem(
                id=response["_id"],
                text=response["_source"]["text"],
                metadata=response["_source"].get("metadata"),
                embedding=response["_source"].get(self.vector_field)
            )
        response = self.client.search(
            index=index,
            size="1000",
            body={"query": {"match_all": {}}}
        )
        if response["hits"]["total"]["value"] == 0:
            return []
        return [
            TextItem(
                id=hit["_id"],
                text=hit["_source"]["text"],
                metadata=hit["_source"].get("metadata"),
                embedding=hit["_source"].get(self.vector_field)
            )
            for hit in response["hits"]["hits"]
        ]

    def semantic_search(
        self, index: str,
        vector: List[float],
        k: int
    ) -> List[TextItem]:

        response = self.client.search(
            index=index,
            knn={
                "field": self.vector_field,
                "query_vector": vector,
                "k": k,
                "num_candidates": k * 4,
            }
        )
        return self.retrieval_parser(response)

    def retrieval_parser(self, response) -> List[TextItem]:
        output = []
        if len(response["hits"]["hits"]) == 0:
            return response
        else:
            for hit in response["hits"]["hits"]:
                output.append(
                    TextItem(
                        id=hit["_id"],
                        text=hit["_source"]["text"],
                        metadata=hit["_source"].get("metadata"),
                        embedding=hit["_source"].get(self.vector_field)
                    )
                )
        return output
