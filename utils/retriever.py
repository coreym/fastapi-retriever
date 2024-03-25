def get_embedding(openai_client, text):
    """ function to generate vector embeddings with the OpenAI text-embedding-3-small model"""
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
