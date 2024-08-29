# Retrieval Augmented Knowledge Graph Generation
[![License: GNU](https://img.shields.io/badge/License-GNU-yellow.svg)](./LICENSE.md)

RAG system that recieves a Natural Language query as input, and gives a textual response and a related Knowledge Graph (RDF).

## Run with Docker

### Requirements
- docker & docker compose.
- openai api key.

### Clone this repository
```bash
git clone https://github.com/vlermandac/retrieval-augmented-graph-generation-webapp/
cd retrieval-augmented-graph-generation-webapp # enter the repository
```

### Add OpenAI API key as environment variable
```bash
# from the project root directory, add your api key with this command
echo "OPENAI_API_KEY=<your-api-key>" >> .env
```
You can also change more build configuration in the .env file.

### Run the App with Docker Compose
```bash
# depending the OS, the docker compose bin can be one of this two:
docker compose up
docker-compose up
```

## (Optional) Run it locally
It was tested in macos ventura using micromamba.

### Requirements
- conda/mamba/micromamba (one of the previous).
- gcc/g++ >= 12 compiler (no guarantee of working with other compilers).

### Create conda environment and install dependencies
```bash
# from ./searcher/
conda create -n searcher -f conda-lock.yml
conda activate searcher
```

### Run each one of the services
- Build and run the graph with Cmake (./graph/).
- Install dependencies, build and run the front-end with npm (./react-app/).
- Run the python service (./searcher/app.py) with uvicorn.
- Edit the docker-compose.yml file to just build Elasticsearch, then run it.

## 💻 Usage 
If you followed one of the above guides, you should be able to use the app from your browser in [http://localhost:3000/].

First, the house button '⌂' on top-left corner will always take you to the current home page.

### Change setting
You can open and change some settings pressing the gear icon '⚙' on the top-right corner.

Remember to always save the changes after you made them. Otherwise they won't update.

### Load files
Now, to make the app work you need to upload files. This can be easily done from the 'setting' tab.

Depending on the size of the file it can take a while to process.

### Make a query
Write a query in Natural Language in the input text box. Send it with the 'Enter' key.
<img width="600" alt="image1" src="https://github.com/vlermandac/searcher-full/assets/68314874/4450c98c-5234-485b-9db9-dc53a4ad7273">

As a result from your query you'll recieve:
1. A textual answer in Natural Language.
2. A rendered Knowledge Graph.
The sizes of the Graph nodes are based on their 'PageRank' score.
<img width="600" alt="image2" src="https://github.com/vlermandac/searcher-full/assets/68314874/925e9829-3ba0-4059-9de2-179339fdc1de">

## Troubleshooting
- Check the ports that each of the docker containers need are available.
- Be sure you don't have keys or password in your .bashrc o .zshrc that could conlfict with the local env variables.
- [Build memory surpass](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_macos_with_docker_for_mac) 
- Check your global docker settings assign enough resources to containers (tested with default setting of 1 GB max and 2 vCPU max).

## Roadmap
- Improve graph visualization.
- Integrate OCR: image -> pdf.
- Better chunking algorithm.
- CI/CD (github actions).
- Locally-runned LLM.
- Ditch python. Re-write backend.
- Optimize graph (big optimization margin).
- Add kubernetes. LLM, DB, backend, frontend could be clusters or nodes.
- More graph algorithms (community detection and others).
