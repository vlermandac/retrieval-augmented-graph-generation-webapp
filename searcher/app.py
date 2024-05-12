from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from main import Main

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
)


@app.post("/submit")
async def submit(user_query: Annotated[str, Form()]):
    main = Main()
    items = {"rag": main.run("--RAG", query=user_query),
             "ids": main.run("--KG")}
    return items
