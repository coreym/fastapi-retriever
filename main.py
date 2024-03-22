from fastapi import FastAPI
from openai import OpenAI
from pinecone import Pinecone
import utils.retriever as retriever
import os

PINECONE_API_KEY = os.getenv('PINECONE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("demo")
openai_client = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

@app.get("/search/{query}")
def search(query: str):
    embed = retriever.get_embedding(openai_client,query)
    conversations = retriever.get_matches(index,embed,namespace='conversations')
    documents = retriever.get_matches(index,embed,namespace='documents')
    results = {"conversations":[],
                "documents":[]}
    for match in conversations["matches"]:
        results["conversations"].append(match["metadata"]["content"])
    for match in documents["matches"]:
        results["documents"].append(match["metadata"]["content"])
    return results

@app.get("/documents/{query}")
def documents(query: str):
    embed = retriever.get_embedding(openai_client,query)
    results = retriever.get_matches(index,embed,namespace='documents')
    return results.to_dict()

@app.get("/conversations/{query}")
def documents(query: str):
    embed = retriever.get_embedding(openai_client,query)
    results = retriever.get_matches(index,embed,namespace='conversations')
    return results.to_dict()