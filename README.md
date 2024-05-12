# text_to_GDB

## Setup
- Run docker compose.
- Get docker password.
- Get docker cert.
- Fill config.yml and move it to the container
- Run the --setup
- Add files to read to the docker volume shared with the local machine.
- Run main.py --read-files.
- Now the app is ready for usage in port 3000.

## Usage
- Enter the next js app at ... port ...
- Enter your query


## Dependencies outside de environment
- charmbracalet/gum (for pretty logging)

## Design

### Data input
- Expected large list of big pdf files.
- DB server (Elastic Search docker image).
- Automatic text chunking based on a given limit (default: LLM token size limit).
- DB for embbeded text information (maybe a vector DB?).
- Patch the DB APIs if necessary.

### LLM app
- Semi-automated prompt selection.
- LLM information extraction.
- Output parsing.
- Transform output to triplet.
- Triplets embedding and insertion to DB.

### Input queries
- Only communicates with the vector DB.
- Vectorize received queries.
- Return top-k within vector DB.
- Use through API (fastAPI library).

### Front-end
- For the final user.
- Simple web app to make queries and visualize outputs.

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
- Run each app in a node within a single kubernetes cluster.
- Locally-run LLM (maybe would be useful to run it in a different cluster than the other apps).
- Ditch python.

## Env
- conda activate llmenv

## Depricated
### Keep the page number as metadata for the text chunks
1. It adds enough complexity to make the cons surpass the pros.
2. To get a chunk page it is as simple as searching the keywords in the original document.

