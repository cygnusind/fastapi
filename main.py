from fastapi import FastAPI, Request, logger
# import asyncio
import httpx

app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, Niyas!", "message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/test1")
async def test():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
    return response.json



@app.post("/mps")
async def root1(request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        #data = body.decode("utf-8")
        response = await client.post("https://pull.devbakuun.cloud/RDK220/mpsnight/",json=data, headers=headers)
        logger.info(body)
        logger.info(response)
        #response.raise_for_status()
        #,content=body, headers=request.headers
    return response
