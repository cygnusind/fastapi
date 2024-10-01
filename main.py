from fastapi import FastAPI, Request
import requests
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from weasyprint import HTML
import io
from typing import Optional, Dict



# import asyncio
import httpx
#import traceback

app = FastAPI()


class BookingData(BaseModel):
    NAME: str = None
    CHECKIN: str = None
    CHECKOUT: str = None
    DAYOF_CHECKIN: str = None
    DAYOF_CHECKOUT11: str = None
    NO_OF_NIGHTS: str = None
    CHECK_IN_TIME: str = None
    CHECK_OUT_TIME: str = None
    HOTELNAME: str = None
    HOTELADDRESS: str = None
    HOTELPHONE: int = None
    ROOMCOUNT: str = None
    CLIENT: str = None
 
    GUESTCOUNT:str = None
    ROOM_CHARGES: str = None
    INCLUSIONS: str = None
    SUBTOTAL: str = None
    GST_VALUE: str = None
    AMT_TO_BE_PAID: str = None
    PAYMENTMODE: str = None
    #LOCATIONLINK:str
    #IMGLINK:str
    # CANCELLATIONPOLICY:str
    # ADDON_POLICES:str
    # DEFAULT_POLICES:str
    EMPNAME:str = None
    EMPPHONE:str = None
    EMPEMAIL:str =None
    TABLEDATA: Optional[Dict[str, list]] = None
    SHOWTRAIFF:str = None





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

    # HTML table structure
    table = """<table style="border-collapse: collapse; width: 100%; border: 1px solid black; font-size:16px;">
        <tr style="background-color: #f2f2f2;">
        <th style="border: 1px solid black; text-align: left; padding: 8px;">Guest NAME</th>
        <th style="border: 1px solid black; text-align: left; padding: 8px;">Room Type</th>
        <th style="border: 1px solid black; text-align: left; padding: 8px;">Occupancy</th>
        <th style="border: 1px solid black; text-align: left; padding: 8px;">Meal Plan</th>
        </tr>"""

    num_rows = len(data.TABLEDATA["GUESTNAME"])

    # Create a new row for each guest
    for i in range(num_rows):
        guest_name = data.TABLEDATA.get("GUESTNAME", [""])[i]
        room_type = data.TABLEDATA.get("ROOMTYPE", [""])[i]
        occupancy = data.TABLEDATA.get("OCC", [""])[i]
        meal_plan = data.TABLEDATA.get("MEALPLAN", [""])[i]
        new_row = f"""<tr>
            <td style="border: 1px solid black; text-align: left; padding: 8px;">{guest_name}</td>
            <td style="border: 1px solid black; text-align: left; padding: 8px;">{room_type}</td>
            <td style="border: 1px solid black; text-align: left; padding: 8px;">{occupancy}</td>
            <td style="border: 1px solid black; text-align: left; padding: 8px;">{meal_plan}</td>
        </tr>"""
        table += new_row

    # Close the table
    table += "</table>"

    replacements = {
        "{{ name }}": data.NAME,
        "{{checkindate}}": data.CHECKIN,
        "{{checkoutdate}}": data.CHECKOUT,
        "{{dayofcheckin}}": data.DAYOF_CHECKIN,
        "{{dayofcheckout}}": data.DAYOF_CHECKOUT11,
        "{{no_of_night}}": data.NO_OF_NIGHTS,
        "{{checkintime}}": data.CHECK_IN_TIME,
        "{{checkouttime}}": data.CHECK_OUT_TIME,
        "{{hotelname}}": data.HOTELNAME,
        "{{hoteladdress}}": data.HOTELADDRESS,
        "{{hotelphone}}": str(data.HOTELPHONE) if data.HOTELPHONE else "",
        "{{noofrooms}}": data.ROOMCOUNT,
        "{{noofguest}}": data.GUESTCOUNT,
        "{{roomcharges}}": data.ROOM_CHARGES,
        "{{inclusions}}": data.INCLUSIONS,
        "{{gst}}": data.GST_VALUE,
        "{{SUBTOTAL}}": data.SUBTOTAL,
        "{{grandtotal}}": data.AMT_TO_BE_PAID,
        "{{PAYMENTMODE}}": data.PAYMENTMODE,
        "{{EMPNAME}}": data.EMPNAME,
        "{{EMPPHONE}}": data.EMPPHONE,
        "{{EMPEMAIL}}": data.EMPEMAIL,
        "{{GUESTTABLE}}": table,
        "{{SHOWTRAIFF}}": data.SHOWTRAIFF
    }

    # if data.PAYMENTMODE == "Bill to Company":
    #     if data.SHOWTRAIFF == "Yes":
    #         replacements.update({
    #             "{{roomcharges}}": data.ROOM_CHARGES,
    #             "{{inclusions}}": data.INCLUSIONS,
    #             "{{gst}}": data.GST_VALUE,
    #             "{{SUBTOTAL}}": data.SUBTOTAL,
    #             "{{grandtotal}}": data.AMT_TO_BE_PAID,
             
            
    #         })
    #     elif data.SHOWTRAIFF == "No":
    #         replacements = {
    #        """<tr><td>Room Charges</td><td style='text-align: right'>{{roomcharges}}</td></tr>
    #         <tr><td>Inclusion IX</td><td style='text-align: right'>{{inclusions}}</td></tr>
    #         <tr><td>Subtotal</td><td style='text-align: right'>{{SUBTOTAL}}</td></tr>
    #         <tr><td>Tax</td><td style='text-align: right'>{{gst}}</td></tr>
    #         <tr><td><b>GRAND TOTAL</b></td><td style='text-align: right'><b>{{grandtotal}}</b></td></tr>":"""
    #         }
    # else:
    #     replacements.update({
    #        """<tr><td>Room Charges</td><td style='text-align: right'>{{roomcharges}}</td></tr>
    #         <tr><td>Inclusion IX</td><td style='text-align: right'>{{inclusions}}</td></tr>
    #         <tr><td>Subtotal</td><td style='text-align: right'>{{SUBTOTAL}}</td></tr>
    #         <tr><td>Tax</td><td style='text-align: right'>{{gst}}</td></tr>
    #         <tr><td><b>GRAND TOTAL</b></td><td style='text-align: right'><b>{{grandtotal}}</b></td></tr>":"""
    #     })

    for placeholder, value in replacements.items():
        if value:
            html_content = html_content.replace(placeholder, value)

    # Generate PDF
    pdf = generate_pdf_from_html(html_content)

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