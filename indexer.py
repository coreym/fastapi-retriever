import os
import pandas as pd
from openai import OpenAI

CHUNK_SIZE=15
PINECONE_API_KEY = os.getenv('PINECONE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_KEY')
PINECONE_INDEX = "testindex"

client = OpenAI(
      api_key=OPENAI_API_KEY
)

def get_embeddings_batch(list):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        dimensions=1536,
        input=list    
    )
    return response

# import csv data, get embeddings by chunk, append to dataframe, write out a copy to CSV
def process_csv(input_file, input_column_index, output_file):
    """
    Processes a CSV file to append an embeddings column to each row.

    Note: This function relies on the assumption that the embeddings API returns embeddings in the exact
    same order as the text was submitted for processing.

    Parameters:
    - input_file (str): The path to the input CSV file.
    - input_column_index (int): The pandas column index containing the text to be embedded.
    - output_file (str): The path where the output CSV file, with the embeddings appended, will be saved.

    Returns:
    - pd.DataFrame: The final concatenated DataFrame with embeddings appended as a new column.

    Example:
    process_csv('input.csv', 'text_to_be_embedded', 'output_with_embeddings.csv')
    """
    dflist = []
    for chunk in pd.read_csv(input_file, chunksize=CHUNK_SIZE,engine='python'):
        tempdf = chunk
        embeddingslist = []
        embeddings = get_embeddings_batch(chunk[input_column_index].tolist())
        for i in embeddings.data: 
            embeddingslist.append(i.embedding)
        tempdf['embedding']=embeddingslist
        dflist.append(tempdf)
    # Note: depends on OpenAI Embeddings API returning embeddings in the same order as they were submitted:
    df_with_embeddings = pd.concat(dflist) 
    df_with_embeddings.to_csv(output_file) 
    return df_with_embeddings
    
def upsert_to_pinecone(pc_client,df,index_col,metadata_col,embedding_col,namespace,PINECONE_BATCHSIZE=100):
    """
    Processes a pandas dataframe (from process_csv()) to upsert to a pinecone index. 

    Parameters:
    - pc_client: a Pinecone Index object
    - df: the dataframe from process_csv()
    - index_col: the column containing a unique ID for the pinecone record
    - metadata_col: the column containing the raw string data to include in the record metadata
    - embedding_col: column of vector embedding lists
    - namespace: pinecone index namespace
    - PINECONE_BATCHSIZE: number of records to upsert at a time
    """
    for i in range(0, len(df), PINECONE_BATCHSIZE):
     # Get the current chunk of data.
        batch = df[i:i+100]
        batchvectors = []
        for i,row in batch.iterrows(): 
            batchvectors.append(dict(id=str(row[index_col]), 
                                    metadata=dict(conversation=row[metadata_col]),
                                    values=row[embedding_col]))
        #   print(batchvectors[0])
        pc_client.upsert(
            vectors=batchvectors,
            namespace=namespace
        )
    