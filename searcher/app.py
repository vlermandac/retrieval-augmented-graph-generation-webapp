from fastapi import (
    FastAPI, Query, File, UploadFile)
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated, List
from pydantic import BaseModel
from dotenv import load_dotenv
from main import Main
import httpx
import logging
import os
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
cpp_endpoint = str(os.getenv("CPP_ENDPOINT"))

app = FastAPI()
origins = ["http://localhost", "http://localhost:3000", "http://reactapp"]
app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
)


class GetGraphRequest(BaseModel):
    index: str
    values: List[int]


class StringRequest(BaseModel):
    request: str


class ConfigRequest(BaseModel):
    index_name: str
    chat_model: str
    embedding_model: str
    embedding_dimension: int
    chunk_size: int
    chunk_overlap: int
    top_k: int


@app.get("/get-indices")
async def get_indices():
    main = Main()
    return {"indices": main.list_indices()}


@app.get("/get-config")
async def get_config():
    main = Main()
    return main.get_config()


@app.post("/update-config")
async def update_config(new_config: ConfigRequest):
    main = Main()
    return main.update_config(
        index_name=new_config.index_name,
        chat_model=new_config.chat_model,
        embedding_model=new_config.embedding_model,
        embedding_dimension=new_config.embedding_dimension,
        chunk_size=new_config.chunk_size,
        chunk_overlap=new_config.chunk_overlap,
        top_k=new_config.top_k
    )


@app.post("/load-file")
async def load_file(file: UploadFile = File(...)):
    start_time = time.time()
    logger.info("loading file...")
    main = Main()
    file_index = main.ingest_data(file)
    logger.info(f"file successfully ingested with index: {file_index}")
    triplets = main.generate_triplets(file_index).model_dump()
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            f"{cpp_endpoint}/generate",
            headers={"Content-Type": "application/json"},
            json={"index": file_index, "triplet_lists": triplets}
        )
        end_time = time.time()
        logger.info(f"file successfully loaded in {end_time - start_time} seconds")
        return response.text


@app.post("/query-rag")
async def rag(query: StringRequest):
    start_time = time.time()
    logger.info("RAG query received")
    main = Main()
    rag, ids = main.query_rag(query=query.request)
    end_time = time.time()
    logger.info(f"RAG query successfully completed in {end_time - start_time} seconds")
    logger.info(f"RAG: {rag}")
    return {"rag": rag, "ids": ids}


@app.post("/get-graph")
async def update_graph(request: GetGraphRequest):
    start_time = time.time()
    logger.info(f"graph query received for index: {request.index} and values: {request.values}")
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            f"{cpp_endpoint}/get",
            headers={"Content-Type": "application/json"},
            json=request.dict()
        )
        end_time = time.time()
        logger.info(f"graph query successfully completed in {end_time - start_time} seconds")
        # logger.info(f"graph: {response.text}")
        return response.json()


@app.post("/delete-index")
async def delete_index(index: StringRequest):
    main = Main()
    main.delete_index(index.request)
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            f"{cpp_endpoint}/delete",
            headers={"Content-Type": "application/json"},
            json={"index": index.request}
        )
        return response.text
