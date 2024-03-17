import os
import pandas as pd
import numpy as np
from openai import OpenAI

OPENAI_KEY=os.getenv('OPENAI_KEY')

client = OpenAI(
      api_key=OPENAI_KEY
)

# function to generate vector embeddings with the OpenAI text-embedding-3-large API from local CSV files
def generate_vector_embeddings(input_xls_file, output_csv_file):
    # import necessary libraries

    # load the input CSV file
    df = pd.read_excel(input_xls_file)

    # create a list of the text data
    text_data = df['conversation'].tolist()

    # generate vector embeddings for the text data
    vector_embeddings = []
    for text in text_data: 
        response = client.embeddings.create(
        model="text-embedding-3-small",
        dimensions=1536,
        input=text    # return_numpy=True,
    )
    vector_embeddings.append(response['data'][0]['embedding'])
    # convert the list of vector embeddings to a numpy array
    vector_embeddings = np.array(vector_embeddings)

    # add the vector embeddings to the output CSV file
    df['vector_embeddings'] = vector_embeddings

    # save the output CSV file
    df.to_csv(output_csv_file, index=False)

