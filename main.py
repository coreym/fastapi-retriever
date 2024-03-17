from fastapi import FastAPI
from openai import OpenAI
from pinecone import Pinecone
import utils.retriever as retriever
import os

PINECONE_API_KEY = os.getenv('PINECONE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("testindex")
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
    results = retriever.get_matches(index,embed,namespace='servicecloud')
    return results.to_dict()