from fastapi import FastAPI, Request
import requests
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# import asyncio
import httpx
#import traceback

app = FastAPI()


class BookingData(BaseModel):
    name: str

@app.post("/booking-confirmation", response_class=HTMLResponse)
async def booking_confirmation(data: BookingData):
     # Open and read the HTML file
     with open("index1.html", "r") as file:
         html_content = file.read()
    
     # Replace the placeholder with the actual name
     updated_html = html_content.replace("{{ name }}", data.name)

     return HTMLResponse(content=updated_html)

@app.get("/")
async def root():
    print(f"Test")
    return {"greeting": "Hello, Niyas!", "message": "Welcome to FastAPI!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/test1")
async def test():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
    return response.json


@app.post("/create")
async def create_user(request: Request):
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body: {body}")
        #return {"Testresponse": "Test"}
        # Make the request to the external API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://reqres.in/api/users",
                headers={"Content-Type": "application/json"},
                json=body
            )

        # Return the response from the external API
        return response.json()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}
    

@app.post("/getprop")
async def get_prop(request: Request):
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body: {body}")
        # Make the request to the Bakuun API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.bakuun.com/ratedockAPI/RDK220/getproperty",
                headers={"Content-Type": "application/json"},
                json=body
            )

        # Return the response from the Bakuun API
        return response.json()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}

@app.post("/mps")
async def mps_check(request: Request):
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body: {body}")
        #return {"Testresponse": "Test"}
        # Make the request to the Bakuun API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://pull.bakuun.com/RDK220/mpsnight",
                headers={"Content-Type": "application/json"},
                json=body
            )
         # Print raw response text for debugging
        raw_response_text = response.text
        print(f"Raw response text: {raw_response_text}")
        # Return the response from the external API
        return response.json()
    except Exception as e:
         print(f"Unexpected error: {e}")
         return {"error": "Unexpected error occurred"}


#mps seacrh by city
@app.post("/mpscity")
async def mpsc(request: Request):
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body: {body}")
        #return {"Testresponse": "Test"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://pull.bakuun.com/RDK220/mpsnight",
                headers={"Content-Type": "application/json"},
                json=body
            )

        # Return the response from the external API
        return response.json()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}


#mps seacrch results
@app.get("/mpsresult/{token}/results")
async def mps_search(token : str,request: Request):
        
    api_url ="https://pull.bakuun.com/RDK220/mpsnight/"+token+"/results"
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body: {body}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        response = requests.get(api_url, json=body, headers={"Content-Type": "application/json","Accept": "application/json"})
        print(f"Response: {response}")

        # Return the response from the external API
        return response
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}     

        
           
@app.post("/sps")
async def sps(request: Request):
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body: {body}")
        #return {"Testresponse": "Test"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://pull.bakuun.com/RDK220/spsnight",
                headers={"Content-Type": "application/json"},
                json=body
            )

        # Return the response from the external API
        return response.json()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}
    
@app.get("/sps/{token}/results")
async def sps_token(token : str,request: Request):
    api_url = "https://pull.bakuun.com/RDK220/spsnight/" + token +"/results"
    print(f"API URL: {api_url}")
    try:
        if not await request.body():
            return {"error": "Request body is empty1:" +request}
        body = await request.json()
        print(f"Request body: {body}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    try:
        if not await request.body():
            return {"error": "Request body is empty2"+request}
        body = await request.json()
        print(f"Successfull Request body: {body}")
        #return {"Testresponse": "Test"}
        response = requests.get(api_url, json=body, headers={"Content-Type": "application/json","Accept": "application/json"})
        print(f"Response: {response.text}")
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(
        #         api_url,
        #         headers={"Content-Type": "application/json","Accept": "application/json"},
        #         json=body
        #     )

        # Return the response from the external API
        return response.json()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}

@app.post("/booking")
async def booking(request: Request):
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body: {body}")
        #return {"Testresponse": "Test"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://pull.bakuun.com/ratedockPull/RDK220/booking",
                headers={"Content-Type": "application/json"},
                json=body
            )

        # Return the response from the external API
        return response.json()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}