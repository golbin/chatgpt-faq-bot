import json
from fastapi import FastAPI, Response
from models import Query
from fastapi.middleware.cors import CORSMiddleware

import vectordb


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

faq_db = vectordb.load("prompt-faq.csv")


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    with open('ai-plugin.json', 'r') as f:
        text = f.read()
        return Response(content=text, media_type="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    with open("openapi.yaml") as f:
        text = f.read()
        return Response(content=text, media_type="text/yaml")


@app.post("/query")
async def query(query: Query):
    vector = vectordb.get_embedding(query.query)

    result = vectordb.search(vector, faq_db)

    return {
        'results': result[:query.top_k]
    }
