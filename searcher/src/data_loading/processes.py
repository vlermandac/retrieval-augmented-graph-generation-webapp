from typing import List, Dict, Any
import fitz
import os
import sys

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(pwd, '../src'))
from core_classes import Text, DatabaseClient  # noqa


def read_documents(dir_path: str) -> List[Text]:
    documents = []
    for filename in filter(lambda f: f.endswith('.pdf'), os.listdir(dir_path)):
        file_path = os.path.join(dir_path, filename)
        print(f"Reading {file_path}...")
        with fitz.open(file_path) as doc:
            text = '\n'.join(page.get_text() for page in doc)
        documents.append(Text(id=filename.split('-')[1].split('.')[0].lower(),
                              text=text, metadata={'file_name': file_path}))
    return documents


def index_document(document: Text, client: DatabaseClient) -> Text:
    file_name = document.metadata['file_name'].split('/')[-1]
    document.metadata = {
        'document_name': file_name.split('-')[1].split('.')[0].lower(),
        'author': file_name.split('-')[0].lower()
    }
    client.index(index='document', text=document)
    return document


def chunking(document: Text, chunk_size: int, chunk_overlap: int) -> List[Text]:
    return [
        document.create_child(new_id=str(i), new_text=document.text[start:start + chunk_size])
        for i, start in enumerate(range(0, len(document.text), chunk_size - chunk_overlap))
    ]


def add_embedding(texts: List[Text], embedding_model: str, dims: int, client) -> List[Text]:
    for text in texts:
        response = client.embeddings.create(
            input=text.text,
            model=embedding_model,
            dimensions=dims
        )
        text.embedding = response.data[0].embedding
        print(f"\rEmbedding {text.id}...{round((int(text.id)+1)/len(texts)*100, 2)}%", end="")
    return texts


def index_chunks(texts: List[Text], index_mapping: Dict[str, Any], client: DatabaseClient) -> List[Text]:
    index_name = f"{texts[0].metadata['document_name']}-chunk"
    client.create_index(name=index_name, settings=index_mapping)

    for text in texts:
        response = client.index(index=index_name, text=text)
    return texts
