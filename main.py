from fastapi import FastAPI
# import asyncio
import httpx
from typing import Union
from enum import Enum
from pydantic import BaseModel, Field
from pydantic.config import ConfigDict
from typing_extensions import Annotated
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
#GET PROPERTY
@app.post("/Getproperty/")
async def GetProperty(proid:str):
    async with httpx.AsyncClient() as client:
        payload = {
    "authentication": {
        "username": "cygnus",
        "password": "KdFoGuC_",
        "propertyId": proid,
        "partnerId": "RDK220"
    },
    "action": "GetPropertyInfo"
}
        headers = {
    "accept": "application/json",
    "content-type": "application/json"
}
        
        response = await client.post("https://api.bakuun.com/ratedockAPI/RDK220/getproperty" ,json=payload,headers=headers)


    return response.json()




#MPS
class mutliSeacrhIds(str,Enum):
    propertyIds: str

class ratesByOccupancy1(BaseModel):
   occupancies:list

class MainModal(BaseModel):
    username:str
    password:str
    partnerId:str
    multiSearchByIds:mutliSeacrhIds
    ratesByOccupancy:ratesByOccupancy1

headers = {
    "accept": "application/json",
    "content-type": "application/json"
}
@app.post("/mps")
async def mutli_pro():
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.bakuun.com/ratedockAPI/RDK220/getproperty" ,json=MainModal,headers=headers)
        return MainModal
   
