from fastapi import FastAPI, Request
import requests
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel
from weasyprint import HTML,CSS

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
    HOTELPHONE: str = None
    ROOMCOUNT: str = None
    CLIENT: str = None
 
    GUESTCOUNT:str = None
    ROOM_CHARGES: str = None
    INCLUSIONS: str = None
    SUBTOTAL: str = None
    GST_VALUE: str = None
    AMT_TO_BE_PAID: str = None
    PAYMENTMODE: str = None
    LOCATIONLINK:str = None
    #IMGLINK:str
    CANCELLATIONPOLICY:str=None
    ADDON_POLICES:str = None 
    DEFAULT_POLICES:str = None    
    EMPNAME:str = None
    EMPPHONE:str = None
    EMPEMAIL:str =None
    TABLEDATA: Optional[Dict[str, list]] = None
    SHOWTRAIFF: str = None
    CLIENT_GST:str = None
    FILENAME:str = None
    Booking_Date:str = None
    Booking_Id:str = None
    Brid:str=None
    GST_PRECENT:str =None




def generate_pdf_from_html(html_content):
    pdf_io = io.BytesIO()
    
    # Create a PDF from the HTML content
    HTML(string=html_content).write_pdf(pdf_io,presentational_hints=True)
    
    # Set the cursor back to the start of the BytesIO object
    pdf_io.seek(0)
    return pdf_io


@app.post("/booking-confirmation")
async def booking_confirmation(data: BookingData):
    # Open and read the HTML file
    with open("voucher.html", "r") as file:
        html_content = file.read()

    # HTML table structure
    table = """<table style="border-collapse: collapse; width: 100%; border: 0px solid #dddddd; font-size:16px;">
        <tr>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">S.no</th>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">Guest Name</th>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">Room Type</th>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">Occupancy</th>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">Meal Plan</th>
        </tr>"""

    num_rows = len(data.TABLEDATA["GUESTNAME"])

    # Create a new row for each guest
    for i in range(num_rows):
        s_no = i + 1
        guest_name = data.TABLEDATA.get("GUESTNAME", [""])[i]
        room_type = data.TABLEDATA.get("ROOMTYPE", [""])[i]
        occupancy = data.TABLEDATA.get("OCC", [""])[i]
        meal_plan = data.TABLEDATA.get("MEALPLAN", [""])[i]
        new_row = f"""<tr>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{s_no}</td>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{guest_name}</td>
            <td style="border: 0px solid #dddddd; text-align:center; padding: 8px;">{room_type}</td>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{occupancy}</td>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{meal_plan}</td>
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
        "{{ADDON_POLICES}}": data.ADDON_POLICES,
        "{{DEFAULT_POLICES}}": data.DEFAULT_POLICES,
        "{{CANCELLATIONPOLICY}}": data.CANCELLATIONPOLICY,
        "{{EMPNAME}}": data.EMPNAME,
        "{{EMPPHONE}}": data.EMPPHONE,
        "{{EMPEMAIL}}": data.EMPEMAIL,
        "{{location}}": data.LOCATIONLINK,
        "{{GUESTTABLE}}": table,
        "{{client}}": data.CLIENT,
        "{{clientgst}}": data.CLIENT_GST,
        "{{booking_date}}": data.Booking_Date,
        "{{booking_id}}": data.Booking_Id,
        "{{Brid}}":data.Brid,
        "{{gstpre}}":data.GST_PRECENT
    }

    if data.PAYMENTMODE == "Bill to Company":
        if data.SHOWTRAIFF == "Yes":
            replacements = {
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
        else: 
            # if data.ROOM_CHARGES and data.INCLUSIONS and data.SUBTOTAL and data.GST_VALUE and data.AMT_TO_BE_PAID:
            html_content = html_content.replace("""<table style="max-width:552px;width:100%;"><tbody><tr><td>Room Charges</td><td style="text-align: right">{{roomcharges}}</td></tr><tr><td>Inclusion</td><td style="text-align: right">{{inclusions}}</td></tr><tr><td>Subtotal</td><td style="text-align: right">{{SUBTOTAL}}</td></tr><tr><td>Tax(gst)</td><td style="text-align: right">{{gst}}</td></tr><tr><td><b>GRAND TOTAL</b></td><td style="text-align: right"><b>{{grandtotal}}</b></td></tr></tbody></table>""", "")
       

    if not data.ADDON_POLICES and not data.DEFAULT_POLICES:
        html_content = html_content.replace("""<div class="info-section"><h4>Policies:</h4><p>{{ADDON_POLICES}} <br />{{DEFAULT_POLICES}}</p></div>""", "")


    # Replace placeholders in the HTML content with actual values
    for placeholder, value in replacements.items():
        if value:
            html_content = html_content.replace(placeholder, value)

    # Generate PDF
    pdf = generate_pdf_from_html(html_content)
    filename1 = data.FILENAME+".pdf"
    # Return the PDF as a StreamingResponse
    
    return StreamingResponse(pdf, media_type="application/pdf", headers={"Content-Disposition": "inline; filename="+filename1})


#for vochuer for email
class BookingDataMail(BaseModel):
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
    HOTELPHONE: str = None
    ROOMCOUNT: str = None
    CLIENT: str = None
    
 
    GUESTCOUNT:str = None
    ROOM_CHARGES: str = None
    INCLUSIONS: str = None
    SUBTOTAL: str = None
    GST_VALUE: str = None
    AMT_TO_BE_PAID: str = None
    PAYMENTMODE: str = None
    LOCATIONLINK:str = None
    #IMGLINK:str
    CANCELLATIONPOLICY:str=None
    ADDON_POLICES:str=None
    DEFAULT_POLICES:str=None
    EMPNAME:str = None
    EMPPHONE:str = None
    EMPEMAIL:str =None
    TABLEDATA: Optional[Dict[str, list]] = None
    SHOWTRAIFF: str = None
    CLIENT_GST:str = None
    FILENAME:str = None
    Booking_Date:str = None
    Booking_Id:str = None
    Brid:str=None
    GST_PRECENT:str = None





@app.post("/booking-confirmation-mail")
async def booking_confirmation1(data: BookingDataMail):
    # Open and read the HTML file
    with open("voucherMail.html", "r") as file:
        html_content = file.read()

    # HTML table structure
    table = """<table style="border-collapse: collapse; width: 100%; border: 0px solid #dddddd; font-size:16px;">
        <tr>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">S.no</th>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">Guest Name</th>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">Room Type</th>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">Occupancy</th>
        <th style="border: 0px solid #dddddd; text-align: center; padding: 8px;">Meal Plan</th>
        </tr>"""

    num_rows = len(data.TABLEDATA["GUESTNAME"])

    # Create a new row for each guest
    for i in range(num_rows):
        s_no = i + 1
        guest_name = data.TABLEDATA.get("GUESTNAME", [""])[i]
        room_type = data.TABLEDATA.get("ROOMTYPE", [""])[i]
        occupancy = data.TABLEDATA.get("OCC", [""])[i]
        meal_plan = data.TABLEDATA.get("MEALPLAN", [""])[i]
        new_row = f"""<tr>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{s_no}</td>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{guest_name}</td>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{room_type}</td>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{occupancy}</td>
            <td style="border: 0px solid #dddddd; text-align: center; padding: 8px;">{meal_plan}</td>
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
        "{{ADDON_POLICES}}": data.ADDON_POLICES,
        "{{DEFAULT_POLICES}}": data.DEFAULT_POLICES,
        "{{CANCELLATIONPOLICY}}": data.CANCELLATIONPOLICY,
        "{{EMPNAME}}": data.EMPNAME,
        "{{EMPPHONE}}": data.EMPPHONE,
        "{{EMPEMAIL}}": data.EMPEMAIL,
        "{{location}}": data.LOCATIONLINK,
        "{{GUESTTABLE}}": table,
        "{{client}}": data.CLIENT,
        "{{clientgst}}": data.CLIENT_GST,
        "{{booking_date}}": data.Booking_Date,
        "{{booking_id}}": data.Booking_Id,
        "{{BRID}}":data.Brid,
        "{{GST_PRECENT}}":data.GST_PRECENT
    
    }

    if data.PAYMENTMODE == "Bill to Company":
        if data.SHOWTRAIFF == "Yes":
            replacements = {
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
        else: 
            html_content = html_content.replace("""<table style="border-collapse:collapse; width:100%" width="100%"><tbody><tr><td style="padding:10px 0; word-wrap:break-word">Room Charges</td><td style="padding:10px 0; word-wrap:break-word; text-align:right" align="right">{{roomcharges}}</td></tr><tr><td style="padding:10px 0; word-wrap:break-word">Inclusion IX</td><td style="padding:10px 0; word-wrap:break-word; text-align:right" align="right">{{inclusions}}</td></tr><tr><td style="padding:10px 0; word-wrap:break-word">Subtotal</td><td style="padding:10px 0; word-wrap:break-word; text-align:right" align="right">{{SUBTOTAL}}</td></tr><tr><td style="padding:10px 0; word-wrap:break-word">Tax( {{GST_PRECENT}} )</td><td style="padding:10px 0; word-wrap:break-word; text-align:right" align="right">{{gst}}</td></tr><tr><td style="padding:10px 0; word-wrap:break-word"><b>GRAND TOTAL</b></td><td style="padding:10px 0; word-wrap:break-word; text-align:right" align="right"><b>{{grandtotal}}</b></td></tr></tbody></table>""", "")
       
        

    # Replace placeholders in the HTML content with actual values
    for placeholder, value in replacements.items():
        if value:
            html_content = html_content.replace(placeholder, value)

   
    
    return HTMLResponse(content=html_content, status_code=200)




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
    
@app.post("/sps/{token}/results")
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

@app.post("/ack-booking")
async def ackbooking(request: Request):
    try:
        if not await request.body():
            return {"error": "Request body is empty"}
        body = await request.json()
        print(f"Request body[ACK]: {body}")
        #return {"Testresponse": "Test"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.bakuun.com/ratedockAPI/RDK220/booking",
                headers={"Content-Type": "application/json"},
                json=body
            )

        # Return the response from the external API
        return response.json()
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"error": "Unexpected error occurred"}

