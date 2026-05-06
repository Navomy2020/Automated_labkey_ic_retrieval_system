from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from models.key_models import get_all_lab_names, get_currently_issued_labs, approve_transfer_in_db
from services import get_lab_status_response, notify_holder_service

chatbot_bp = Blueprint("chatbot", __name__)
PENDING_ACTIONS = {}

@chatbot_bp.route("/", methods=["GET"])
def index():
    return "<h1>Digital Lab Assistant is Online</h1><p>Webhook active at /whatsapp</p>"

@chatbot_bp.route("/whatsapp", methods=["POST"])
def whatsapp_bot():
    incoming_msg = request.values.get("Body", "").strip().lower()
    phone_number = request.values.get("From")
    resp = MessagingResponse()
    msg = resp.message()

    try:
        current_labs = get_all_lab_names()
        lab_list_lower = [lab.lower() for lab in current_labs]
    except: current_labs = []

    # 1. MENU: Check Status
    if incoming_msg == "1" or incoming_msg in lab_list_lower:
        if incoming_msg == "1":
            options = "\n".join([f"🔹 {lab}" for lab in current_labs])
            msg.body(f"Select a lab:\n\n{options}")
        else:
            msg.body(get_lab_status_response(incoming_msg))

    # 2. MENU: Transfer
    elif incoming_msg == "2" or incoming_msg == "transfer key":
        issued = get_currently_issued_labs()
        if not issued:
            msg.body("📍 All keys are in the lab.")
        else:
            options = "\n".join([f"🔹 {lab}" for lab in issued])
            msg.body(f"Which key do you need?\n\n{options}")
            PENDING_ACTIONS[phone_number] = "waiting_for_lab"

    # 3. STEP: Request Notification
    elif PENDING_ACTIONS.get(phone_number) == "waiting_for_lab":
        from models.key_models import get_lab_status_details
        status = get_lab_status_details(incoming_msg)
        if "error" in status:
            msg.body("⚠️ Lab not found. Try again.")
        else:
            msg.body(f"Key is with *{status['holder_name']}*.\n\nSend request? (YES/NO)")
            PENDING_ACTIONS[phone_number] = {"state": "confirm_send", "lab": incoming_msg}

    # 4. STEP: Wait for Physical Handover
    elif PENDING_ACTIONS.get(phone_number, {}).get("state") == "confirm_send":
        lab = PENDING_ACTIONS[phone_number]["lab"]
        if incoming_msg == "yes":
            notify_holder_service(phone_number, lab)
            msg.body("📩 Request sent! Go to the holder and take the key. Once you have it, type *CONFIRM*.")
            PENDING_ACTIONS[phone_number] = {"state": "waiting_for_handover", "lab": lab}
        else:
            msg.body("Cancelled."); del PENDING_ACTIONS[phone_number]

    # 5. STEP: Final Confirmation (Updates Database)
    elif PENDING_ACTIONS.get(phone_number, {}).get("state") == "waiting_for_handover":
        if incoming_msg == "confirm":
            lab = PENDING_ACTIONS[phone_number]["lab"]
            if approve_transfer_in_db(phone_number, lab):
                msg.body(f"✅ Success! You are now the official holder of the {lab} key.")
            else:
                msg.body("❌ Error updating database.")
            del PENDING_ACTIONS[phone_number]

    else:
        msg.body("👋 *Lab Assistant*\n1️⃣ Check Status\n2️⃣ Transfer Key")

    return str(resp)