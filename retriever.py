import os
from fastapi import FastAPI
from openai import OpenAI
from pinecone import Pinecone
PINECONE_API_KEY = os.getenv('PINECONE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("pinecone-index")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# function to generate vector embeddings with the OpenAI text-embedding-3-small model
def get_embedding(text):
    # generate vector embeddings for the text data
    response = openai_client.embeddings.create(
    model="text-embedding-3-small",
    dimensions=1536,
    input=text
    )
    return response.data[0].embedding

def get_matches(pinecone_client,query_vector,top_k=3,**kwargs):
    clientargs={
        "vector":query_vector,
        "top_k":top_k,
        "include_metadata":True
    }
    ns = kwargs.get('namespace') #try to get namespace if it was passed
    if ns is not None:
        clientargs['namespace'] = ns
    response = pinecone_client.query(**clientargs)
    return response
# def format_for_gpt(ra)
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/search/{query}")
def search(query: str):
    return f"Searching for {query}..."
