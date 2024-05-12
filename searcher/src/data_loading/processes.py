def index_document(document, client):
    file_name = document.metadata['file_name']
    file_name = file_name.split('/')[-1]
    document.metadata = {
        'document_name': file_name.split('-')[1].split('.')[0].lower(),
        'author': file_name.split('-')[0].lower()
    }
    client.index(
        index='document',
        id=document.metadata['document_name'],
        body={'name': document.metadata['document_name'],
              'author': document.metadata['author'],
              'text': document.text},
        ignore=400
    )
    return document


def update_metadata(nodes):
    for i, node in enumerate(nodes):
        node.id_ = i
    return nodes


def add_embedding(nodes, embedding_model, dims, client):
    for node in nodes:
        response = client.embeddings.create(
            input=node.text,
            model=embedding_model,
            dimensions=dims
        )
        node.metadata['embedding'] = response.data[0].embedding
    return nodes


def index_chunks(nodes, index_mapping, client):
    index_name = f"{nodes[0].metadata['document_name']}-chunks"
    client.indices.create(index=index_name, mappings=index_mapping, ignore=400)
    for node in nodes:
        client.index(
            index=index_name,
            id=node.node_id,
            body={
                'text': node.text,
                'embedding': node.metadata['embedding']
            },
            ignore=400
        )
    return nodes
