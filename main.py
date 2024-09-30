from fastapi import FastAPI, Request
import requests
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from weasyprint import HTML
import io


# import asyncio
import httpx
#import traceback

app = FastAPI()


class BookingData(BaseModel):
    NAME: str
    CHECKIN:str
    CHECKOUT:str
    DAYOF_CHECKIN:str
    DAYOF_CHECKOUT11:str
    NO_OF_NIGHTS:str
    CHECK_IN_TIME:str
    CHECK_OUT_TIME:str
    HOTELNAME:str
    HOTELADDRESS:str
    HOTELPHONE:int
    LOCATIONLINK:str
    IMGLINK:str
    ROOMCOUNT:str
    CLIENT:str
    ROOM_CHARGES:str
    INCLUSIONS:str
    SUBTOTAL:str
    GST_VALUE:str
    AMT_TO_BE_PAID:str
    PAYMENTMODE:str
    CANCELLATIONPOLICY:str
    # ADDON_POLICES:str
    # DEFAULT_POLICES:str
    # EMPNAME:str
    # EMPPHONE:int
    # EMPEMAIL:str


    











def generate_pdf_from_html(html_content):
    pdf_io = io.BytesIO()
    
    # Create a PDF from the HTML content
    HTML(string=html_content).write_pdf(pdf_io)
    
    # Set the cursor back to the start of the BytesIO object
    pdf_io.seek(0)
    return pdf_io


@app.post("/booking-confirmation")
async def booking_confirmation(data: BookingData):
     # Open and read the HTML file
     with open("voucher.html", "r") as file:
         html_content = file.read()
         
         
         updated_html = html_content.replace("{{ name }}", data.NAME)
         updated_html = updated_html.replace("{{checkindate}}", data.CHECKIN)
         updated_html = updated_html.replace("{{checkoutdate}}", data.CHECKOUT)
         updated_html = updated_html.replace("{{dayofcheckin}}", data.DAYOF_CHECKIN)
         updated_html = updated_html.replace("{{dayofcheckout}}", data.DAYOF_CHECKOUT11)
         updated_html = updated_html.replace("{{no_of_night}}", data.NO_OF_NIGHTS)
         updated_html = updated_html.replace("{{checkintime}}", data.CHECK_IN_TIME)
         updated_html = updated_html.replace("{{checkouttime}}", data.CHECK_OUT_TIME)
         updated_html = updated_html.replace("{{hotelname}}", data.HOTELNAME)
         updated_html = updated_html.replace("{{hoteladdress}}", data.HOTELADDRESS)
         updated_html = updated_html.replace("{{location}}", data.LOCATIONLINK)
         updated_html = updated_html.replace("{{hotelphone}}", data.HOTELPHONE)
         updated_html = updated_html.replace("{{imglink}}", data.IMGLINK)
         updated_html = updated_html.replace("{{noofrooms}}", data.ROOMCOUNT)
         updated_html = updated_html.replace("{{noofguest}}", data.CLIENT)
         updated_html = updated_html.replace("{{roomcharges}}", data.ROOM_CHARGES)
         updated_html = updated_html.replace("{{inclusions}}", data.INCLUSIONS)
         updated_html = updated_html.replace("{{gst}}", data.GST_VALUE)
         updated_html = updated_html.replace("{{SUBTOTAL}}", data.SUBTOTAL)
         updated_html = updated_html.replace("{{grandtotal}}", data.AMT_TO_BE_PAID)
         updated_html = updated_html.replace("{{PAYMENTMODE}}", data.PAYMENTMODE)
        #  updated_html = updated_html.replace("{{ADDON_POLICES}}", data.ADDON_POLICES)
        #  updated_html = updated_html.replace("{{DEFAULT_POLICES}}", data.DEFAULT_POLICES)
         updated_html = updated_html.replace("{{CANCELLATIONPOLICY}}", data.CANCELLATIONPOLICY)

        # updated_html = updated_html.replace("{{EMPNAME}}", data.EMPNAME)
        #  updated_html = updated_html.replace("{{EMPPHONE}}", data.EMPPHONE)
        #  updated_html = updated_html.replace("{{EMPEMAIL}}", data.EMPEMAIL)



 
         

     # Generate PDF
     pdf = generate_pdf_from_html(updated_html)

     # Return the PDF as a StreamingResponse
     return StreamingResponse(pdf, media_type="application/pdf", headers={"Content-Disposition": "inline; filename=booking_confirmation.pdf"})

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