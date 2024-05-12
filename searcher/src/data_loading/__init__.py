from .processes import index_document, add_embedding, index_chunks, update_metadata  # noqa: F401
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader


def run(Client, path, chunk_size, overlap, embedding_model, dims):

    chunk_mapping = {
        "properties": {
            "text": {"type": "text"},
            "embedding": {"type": "dense_vector", "dims": dims}
        }
    }

    es_client = Client.elastic_search()
    oa_client = Client.open_ai()

    chunking = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )

    reader = SimpleDirectoryReader(
        input_dir=path,
        required_exts=[".pdf"],
        file_metadata=lambda filename: {"file_name": filename}
    )

    docs_nodes = []

    for document in reader.load_data():
        doc = index_document(document, es_client)
        nodes = chunking.get_nodes_from_documents([doc])
        update_metadata(nodes)
        add_embedding(nodes, embedding_model, dims, oa_client)
        index_chunks(nodes, chunk_mapping, es_client)
        docs_nodes.append(nodes)

    return docs_nodes
