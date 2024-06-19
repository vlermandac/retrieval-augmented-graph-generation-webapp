from fastapi import FastAPI, Form, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from pydantic import BaseModel
from dotenv import load_dotenv
from main import Main
import httpx
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()
cpp_endpoint = str(os.getenv("CPP_ENDPOINT"))

app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
)


class GetGraphRequest(BaseModel):
    index: str
    values: Annotated[list[int] | None, Query()] = None


class StringRequest(BaseModel):
    request: str


@app.get("/get-indices")
async def get_indices():
    main = Main()
    return {"files": main.list_indices()}


@app.get("/get-config")
async def get_config():
    main = Main()
    return main.get_config()


@app.post("/update-config")
async def update_config(new_config):
    main = Main()
    return main.update_config(new_config)


@app.post("/load-file")
async def load_file(file: UploadFile = File(...)):
    main = Main()
    file_index = main.ingest_data(file)
    triplets = main.generate_triplets(file_index).dict()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{cpp_endpoint}/generate",
            headers={"Content-Type": "application/json"},
            json={"index": file_index, "triplet_lists": triplets}
        )
        return response.text


@app.post("/query-rag")
async def rag(query: StringRequest):
    main = Main()
    rag, ids = main.query_rag(query=query.request)
    return {"rag": rag, "ids": ids}


@app.post("/get-graph")
async def update_graph(request: GetGraphRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{cpp_endpoint}/get",
            headers={"Content-Type": "application/json"},
            json=request.dict()
        )
        return response.json()


@app.post("/delete-index")
async def delete_index(index: StringRequest):
    main = Main()
    main.delete_index(index.request)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{cpp_endpoint}/delete",
            headers={"Content-Type": "application/json"},
            json={"index": index.request}
        )
        return response.text
