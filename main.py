from fastapi import FastAPI, Request
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



@app.post("/getprop")
async def root1(request: Request):
  



    async with httpx.AsyncClient() as client:
        headers = {
    "accept": "application/json",
    "content-type": "application/json"
}
  
        body = await request.body()
        data = body.decode("utf-8")
        response = await client.post("https://api.bakuun.com/ratedockAPI/RDK220/getproperty",json=data, headers=headers)
        response.raise_for_status()
        #,content=body, headers=request.headers
    return response.raise_for_status()
