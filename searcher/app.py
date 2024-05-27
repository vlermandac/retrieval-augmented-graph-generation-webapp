from typing import Annotated
from fastapi import FastAPI, Form, Query
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


@app.get("/load-data")
async def load_data():
    main = Main()
    main.run("--load_data")
    return {"status": "Documents from './data' loaded."}


@app.get("/triplets")
async def triplets():
    main = Main()
    triplets = main.run("--triplets")
    print("Triplets generated at '../data/triplets.json'")
    return {"triplets": triplets}


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


@app.post("/rag")
async def rag(query: Annotated[str, Form()]):
    main = Main()
    rag, ids = main.run("--RAG", query=query)
    return {"rag": rag, "ids": ids}
