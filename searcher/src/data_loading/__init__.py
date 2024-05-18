from .processes import read_documents, index_document, chunking, add_embedding, index_chunks  # noqa: F401


def run(Client, unprocessed_files, chunk_size, overlap, embedding_model, dims):

    chunk_mapping = {
        "properties": {
            "text": {"type": "text"},
            "embedding": {"type": "dense_vector", "dims": dims}
        }
    }

    es_client = Client.elastic_search()
    oa_client = Client.open_ai()

    documents = read_documents(unprocessed_files)
    docs_chunks = []
    for doc in documents:
        index_document(doc, es_client)
        chunks = chunking(doc, chunk_size, overlap)
        chunks = add_embedding(chunks, embedding_model, dims, oa_client)
        index_chunks(chunks, chunk_mapping, es_client)
        docs_chunks.append(chunks)

    return docs_chunks
