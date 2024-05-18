# text_to_GDB

## Requirements
- Docker.
- Conda.
- charmbracalet/gum (optional for pretty logging)

## Setup

### Run elasticsearch with Docker

```bashrc
docker network create elastic
```

```bashrc
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.4
docker pull docker.elastic.co/kibana/kibana:8.13.4
```

```bashrc
docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.13.4
docker run --name kib01 --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.13.4
```

In case you lost one of this two:
```bashrc
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

```bashrc
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
```
Be sure you don't have keys or password in your .bashrc o .zshrc that could conlfict with the local env variables.

### Backend
./searcher

#### Env
- conda activate llmenv
- install environment.yml

- Fill searcher/config.yml and move it to the container
- Add the pdf files you want to load to elasticsearch in the data directory.
- Load them with python main --load_data
- docker exec fastapi sh -c "uvicorn app:app --host localhost --port 8000"

### Frontend
./react-app/
- Run vite + react project with Docker.
- Now the app is ready for usage in port 3000.

## Usage
- Enter your query

## Roadmap

- Improve classes:
    - Static typing and functions with pydantic.
    - method/propery decorators.
- Better documents and document chunks structure.
    - Improve serialization.
- File agnostic.

### Mid-term
- Hallucination validation.
- CI/CD (github actions).

### Long-term
- Locally run LLM.
- Ditch python. Re write from scracth in rust.
- Add kubernetes. LLM, DB, backend, frontend could be clusters or nodes.


## Depricated
### Keep the page number as metadata for the text chunks
1. It adds enough complexity to make the cons surpass the pros.
2. To get a chunk page it is as simple as searching the keywords in the original document.

