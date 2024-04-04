# FastAPI based Retriever/Indexer service over Pinecone, optimized for deployment on render.com

## Manual Steps

1. Index your data in Pinecone with openAI text-embedding-3-small (sample notebook coming)
2. Create a new Web Service on Render.
3. Populate the OPENAI_KEY and PINECONE_KEY environment variables with your API keys.
4. Specify the URL to this repository
5. Render will automatically detect that you are deploying a Python service and use `pip` to download the dependencies.
6. Specify the following as the Start Command.

    ```shell
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```

7. Click Create Web Service.

Or simply click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/render-examples/fastapi)

## Thanks

Thanks to [Harish](https://harishgarg.com) for the [inspiration to create a FastAPI quickstart for Render](https://twitter.com/harishkgarg/status/1435084018677010434) and for some sample code!
