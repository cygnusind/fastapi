from fastapi import FastAPI
import asyncio
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
    return response.json()

@app.post("/Getproperty")
async def test1():
    async with httpx.AsyncClient() as client:
        payload = {
    "authentication": {
        "username": "cygnus",
        "password": "KdFoGuC_",
        "propertyId": "HTL993.6",
        "partnerId": "RDK220"
    },
    "action": "GetPropertyInfo"
}
        headers = {
    "accept": "application/json",
    "content-type": "application/json"
}
        
        response = await client.post("https://api.bakuun.com/ratedockAPI/RDK220/getproperty" ,headers=headers,data=payload)
      

    return response.json()
   
