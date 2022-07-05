from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()


@app.get("/")
async def hello():
    return Response("Hello, FastAPI!")
