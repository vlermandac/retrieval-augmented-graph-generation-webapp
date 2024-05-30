from typing import Annotated
from fastapi import FastAPI, Form, Query, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from main import Main
import httpx

app = FastAPI()

cpp_server_url = "http://localhost:8080"

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:64851",
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
)


class ListRequest(BaseModel):
    values: Annotated[list[int] | None, Query()] = None


class ConfigOptions(BaseModel):
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    chat_model: str
    index_name: str
    top_k: int


@app.post("/update-config")
async def update_config(new_config: ConfigOptions):
    main = Main()
    res = main.update_config(**new_config.dict())
    return {"status": res}


@app.get("/config")
async def get_config():
    main = Main()
    res = main.get_config()
    return res


@app.post("/load-file")
async def load_file(file: UploadFile = File(...)):
    main = Main()
    res = main.run("--load_data", request=file)
    return {"status": res}


@app.get("/list-files")
async def list_files():
    main = Main()
    res = main.list_files()
    return {"files": res}


@app.get("/triplets")
async def triplets():
    main = Main()
    res = main.run("--triplets")
    return {"status": res}


@app.post("/rag")
async def rag(query: Annotated[str, Form()]):
    main = Main()
    rag, ids = main.run("--RAG", request=query)
    return {"rag": rag, "ids": ids}


@app.get("/clear")
async def clear():
    url = f"{cpp_server_url}/generate"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url, headers={"Content-Type": "text/plain"})
    return response.text


@app.post("/update-graph")
async def update_graph(values: ListRequest):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{cpp_server_url}/update",
            headers={"Content-Type": "application/json"},
            json=values.dict())
    return response.json()
