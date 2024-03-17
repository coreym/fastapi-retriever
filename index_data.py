import os
import pandas as pd
from pinecone import Pinecone, ServerlessSpec
PINECONE_KEY=os.getenv('PINECONE_KEY')
pc = Pinecone(api_key=PINECONE_KEY)

indexes = ['conversations', 'articles']
for i in indexes: 
  pc.create_index(
  name=i,
  dimension=1536,
  metric="cosine",
  spec=ServerlessSpec(
    cloud="aws",
    region="us-west-2"
  )
)

