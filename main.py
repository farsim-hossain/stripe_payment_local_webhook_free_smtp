

import os
import stripe
from fastapi import FastAPI, Request, Header
import sqlite3
import secrets
from dotenv import load_dotenv
import requests
import json

load_dotenv()
# Print both the raw and loaded values
print(f"Raw env value: {os.environ.get('SMTP2GO_API_KEY_NEW')}")
SMTP2GO_API_KEY = os.getenv("SMTP2GO_API_KEY_NEW")
print(f"Loaded API Key: {SMTP2GO_API_KEY}")


app = FastAPI()
stripe.api_key = os.getenv("STRIPE_KEY")


SENDER_EMAIL = os.getenv("SENDER_EMAIL")

conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT,
    counter INTEGER)
""")
conn.commit()

def send_email_smtp2go(to_email, password):
    url = "https://api.smtp2go.com/v3/email/send"
    headers = {
        "Content-Type": "application/json",
        "X-Smtp2go-Api-Key": SMTP2GO_API_KEY,
    }
    
    data = {
        "sender": f"XYZ App <{SENDER_EMAIL}>",
        "to": [f"<{to_email}>"],
        "subject": "Your Access Password",
        "html_body": f"""
            <h2>Thank you for your purchase!</h2>
            <p>Your access password is: <strong>{password}</strong></p>
            <p>You can now log in to the application using your email and this password.</p>
        """,
        "text_body": f"Thank you for your purchase! Your access password is: {password}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"SMTP2GO Response: {response.text}")  # This will help debug the response
        return response.status_code == 200
    except Exception as e:
        print(f"Email sending error: {str(e)}")
        return False



from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("checkout.html", {"request": request})
# Add these routes to your main.py
@app.get("/success")
async def success_page(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@app.get("/cancel")
async def cancel_page(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})



@app.post("/create-checkout-session")
async def create_checkout_session(request: Request):
    data = await request.json()
    email = data.get("email")
    
    customer = stripe.Customer.create(email=email)
    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Your Product Name',
                },
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=os.getenv('SUCCESS_URL'),
        cancel_url=os.getenv('CANCEL_URL'),
        customer=customer.id,
        receipt_email=email
    )
    
    return {"id": session.id}

@app.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    data = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(data, stripe_signature, webhook_secret)
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session['customer_details']['email']
            
            # Generate and store password
            password = secrets.token_hex(8)
            
            # Store in database
            with sqlite3.connect("users.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO users (email, password, counter) VALUES (?, ?, 0)",
                    (customer_email, password)
                )
                conn.commit()
            
            # Send email
            email_response = send_email_smtp2go(customer_email, password)
            
            # Log the response
            print(f"Email sending response for {customer_email}: {email_response}")
            
            return {"status": "success", "email_sent": True}
            
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return {"status": "error", "message": str(e)}, 400

    return {"status": "success"}




