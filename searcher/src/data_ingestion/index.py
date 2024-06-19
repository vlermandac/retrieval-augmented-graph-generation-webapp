from core_classes import Database, TextItem
from typing import List


def index_items(db: Database, index: str, items: List[TextItem]) -> None:
    db.create_index(name=index, dims=len(items[0].embedding))
    for item in items:
        db.index(index=index, item=item)
