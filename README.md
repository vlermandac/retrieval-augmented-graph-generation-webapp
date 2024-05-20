# text_to_GDB

## Requirements
- docker.
- docker compose.
- conda/mamba/micromamba.
- charmbracalet/gum (optional for tests pretty logging).
- an openai api key.

## Setup

Tested in macos ventura using micromamba for virtual environments.

### Clone this repository
```bashrc
git clone ... 
cd searcher-full  # enter the repository
```

### Openai API key
```bashrc
# from the project root directory, add the openai api key to the env variables
echo "OPENAI_API_KEY=actualkey" >> .env
```
You can also change more build configuration in the .env file.

### Create conda environment and install dependencies
```bashrc
conda create -n searcher -f searcher/conda-lock.yml
conda activate searcher
```

### Run the app
```bashrc
# internally runs docker compose and uvicorn
./run_app.sh
```

### Load data
By now the app should be working.
Now place some pdf files in the format {author_name-doc_name.pdf} in searcher/data directory. e.g.:
```bashrc
mv somewhere/martin_scorcesse-goodfellas_script.pdf
```
and load to the app with:
```bashrc
curl "http://localhost:8000/load"
```
Now you can use the app from your browser in [http://localhost:3000/].

## Usage
- Configure the app variables in searcher/config.yml.
- Write the query you want to ask the app about some of the texts you loaded
and defined in config.yml in 'index_to_query' field.

As results from your query you will recieve:
1. A answer for the RAG inside the app.
2. A knowledge graph visualization from the doc you are querying.
The edges related to the answer made by the RAG will be displayed in a different color.

## Roadmap

## Troubleshooting
- Be sure you don't have keys or password in your .bashrc o .zshrc that could conlfict with the local env variables.
- Build memory surpass: [https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_macos_with_docker_for_mac]

### Short-term
- Integrate OCR: image -> pdf.
- Improve classes:
    - Static typing and functions with pydantic for all classes (currently 50% approx).
    - ADTs for database and LLM.
- Better chunking algorithm.
- Evaluate knowledge graph creating and RAG with RAGAS.
- Hallucination validation.

### Long-term
- Load data from web app.
- CI/CD (github actions).
- Locally-runned LLM.
- Ditch python. Re write from scracth in Rust.
- Add more option for databases: MongoDB, others vectors DBs.
- Add kubernetes. LLM, DB, backend, frontend could be clusters or nodes.


## Depricated ideas
### Keep the page number as metadata for the text chunks
1. It adds enough complexity to make the cons surpass the pros.
2. To get a chunk page it is as simple as searching the keywords in the original document.

### Dockerize everything
1. Couldn't configure elasticsearch to allow another container to make a request, even with the correct
password, url, and certificates to do so.
2. Thinking in adding kubernetes + containerd would make this unnecesary.
