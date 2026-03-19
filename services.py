
  from twilio.rest import Client
from models.key_models import get_lab_status_details
import os

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_WHATSAPP_NUMBER") 
client = Client(account_sid, auth_token)

def get_lab_status_response(lab_name):
    details = get_lab_status_details(lab_name)
    if "error" in details: return "⚠️ Lab not found."
    return f"📍 *{lab_name}* Status: {details['status']}\n👤 Current Holder: {details.get('holder_name', 'N/A')}"

def notify_holder_service(requester_phone, lab_name):
    """Alerts the current holder via WhatsApp about the incoming request."""
    details = get_lab_status_details(lab_name)
    holder_phone = details.get('holder_phone')
    
    if holder_phone:
        msg_body = f"🔔 *Key Request!*\nA student is coming to collect the *{lab_name}* key from you. Please hand it over when they arrive."
        client.messages.create(from_=f"whatsapp:{twilio_phone}", body=msg_body, to=holder_phone)
    return True