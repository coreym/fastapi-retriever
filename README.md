# FastAPI based Retriever/Indexer service for connecting OpenAI Custom GPTs to a Pinecone vector store. 

## Manual Steps

1. You may use this repository directly or [create your own repository from this template](https://github.com/render-examples/fastapi/generate) if you'd like to customize the code.
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
