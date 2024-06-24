from fastapi import (
    FastAPI, Query, File, UploadFile, Request, HTTPException, status)
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
PASSCODE = str(os.getenv("PASSCODE"))
verified = False

app = FastAPI()
origins = ["http://localhost:3000", "http://fastapi:3000"]
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
)


@app.middleware("http")
async def passcode_middleware(request: Request, call_next):
    if request.url.path not in ["/login"]:
        if verified is False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid passcode",
            )
    response = await call_next(request)
    return response


@app.post("/login")
async def login(request: Request):
    passcode = request.headers.get("x-passcode")
    if passcode == PASSCODE:
        global verified
        verified = True
        return {"message": "Login successful"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="401",
        )


class GetGraphRequest(BaseModel):
    index: str
    values: Annotated[list[int] | None, Query()] = None


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
        return response.text


@app.post("/query-rag")
async def rag(query: StringRequest):
    main = Main()
    rag, ids = main.query_rag(query=query.request)
    return {"rag": rag, "ids": ids}


@app.post("/get-graph")
async def update_graph(request: GetGraphRequest):
    async with httpx.AsyncClient(timeout=None) as client:
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
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            f"{cpp_endpoint}/delete",
            headers={"Content-Type": "application/json"},
            json={"index": index.request}
        )
        return response.text
