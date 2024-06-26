from fastapi import FastAPI, Request
# import asyncio
import httpx
import traceback

app = FastAPI()

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
    
@app.get("/sps/{token}")
async def sps_token(request: Request,token : str):
    api_url = "https://pull.bakuun.com/RDK220/spsnight/" + token + "/results"
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body: {body}")
        #return {"Testresponse": "Test"}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                api_url,
                headers={"Content-Type": "application/json"},
                json=body
            )

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