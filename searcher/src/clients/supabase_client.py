from typing import Optional, Union, List
import vecs
from core_classes import TextItem, Database


class SupabaseClient(Database):
    def __init__(self, SUPABASE_URL: str, SUPABASE_USER: str, SUPABASE_PASSWORD: str):
        DB_CONNECTION = f"postgresql://{SUPABASE_USER}:{SUPABASE_PASSWORD}@{SUPABASE_URL}"
        self.client = vecs.create_client(DB_CONNECTION)
        self.dims = 200

    def create_index(self, name: str, dims: int):
        self.dims = dims
        collection = self.client.get_or_create_collection(name=name, dimension=dims)
        collection.create_index()

    def index(self, index: str, item: TextItem):
        collection = self.client.get_or_create_collection(name=index, dimension=self.dims)
        metadata = item.metadata | {"text": item.text} | {"embedding": item.embedding}
        collection.upsert(records=[(item.id, item.embedding, metadata)])

    def delete(self, index: str, id: Optional[str] = None):
        collection = self.client.get_or_create_collection(name=index, dimension=self.dims)
        if id is not None:
            collection.delete(ids=[id])
        else:
            collection.delete()

    def search(self, index: str, id: Optional[str] = None) -> Union[None, TextItem, List[TextItem]]:
        collection = self.client.get_or_create_collection(name=index, dimension=self.dims)
        if id is not None:
            records = collection.query(filters={"id": {"$eq": id}}, limit=1, include_metadata=True)
            if records:
                metadata = records[0][1].copy()
                text = metadata.pop("text")
                embedding = metadata.pop("embedding")
                return TextItem(
                    id=records[0][0],
                    text=text,
                    embedding=embedding,
                    metadata=metadata
                )
            return None
        else:
            q_vector = [0.5] * self.dims
            records = collection.query(data=q_vector, limit=1000, include_metadata=True)
            items = []
            for i in range(len(records)):
                metadata = records[i][1].copy()
                text = metadata.pop("text")
                embedding = metadata.pop("embedding")
                items.append(
                    TextItem(
                        id=records[i][0],
                        text=text,
                        embedding=embedding,
                        metadata=metadata
                    )
                )
            return items

    def semantic_search(self, index: str, vector: List[float], k: int) -> List[TextItem]:
        collection = self.client.get_or_create_collection(name=index, dimension=self.dims)
        records = collection.query(
            data=vector,
            limit=k,
            measure="cosine_distance",
            include_metadata=True
        )
        items = []
        for i in range(len(records)):
            metadata = records[i][1].copy()
            text = metadata.pop("text")
            embedding = metadata.pop("embedding")
            items.append(
                TextItem(
                    id=records[i][0],
                    text=text,
                    embedding=embedding,
                    metadata=metadata
                )
            )
        return items
