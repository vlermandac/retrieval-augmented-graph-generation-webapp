# text_to_GDB

## Run elasticsearch in docker
docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.4
docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.13.4

docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana

docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .

curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200

Be sure you don't have keys or password in your .bashrc o .zshrc that could conlfict with the local env variables.

## Setup
- Get docker cert.
docker cp elastic:/usr/share/elasticsearch/config/certs/http_ca.crt - | docker cp - fastapi:/app/
- Get docker password.
docker exec -it elastic /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
- Fill searcher/config.yml and move it to the container
docker cp searcher/config.yml fastapi:/app/config.yml
- Run the --setup (enter the llmenv env)
- Add files to read to the docker volume shared with the local machine.
- Run main.py --read-files.
- docker exec fastapi sh -c "uvicorn app:app --host localhost --port 8000"
- Now the app is ready for usage in port 3000.

## Usage
- Enter the next js app at ... port ...
- Enter your query


## Dependencies outside de environment
- charmbracalet/gum (for pretty logging)
- docker
- docker compose

## Roadmap

- Improve classes:
    - Static typing and functions with pydantic.
    - method/propery decorators.
- Better documents and document chunks structure.
    - Improve serialization.
- File agnostic.

### Short-term
- Async functions to get results from gpt
- Knowledge Graph creation with the triples.
- Queries answered with a combination of the stored embeddings and the KG.
- FastAPI deployment.

### Mid-term
- Hallucination validation.
- Instructor integration to validate output.
- CI/CD (github actions).

### Long-term
- Locally run LLM.
- Ditch python. Re write from scracth in rust.
- Add kubernetes. LLM, DB, backend, frontend could be clusters or nodes.

## Env
- conda activate llmenv

## Depricated
### Keep the page number as metadata for the text chunks
1. It adds enough complexity to make the cons surpass the pros.
2. To get a chunk page it is as simple as searching the keywords in the original document.

