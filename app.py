from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from database_config import get_db_connection

app = Flask(__name__)


@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if 'status' in incoming_msg:
        # Example Logic: Check if a specific key is available
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM inventory WHERE item_name='Main Lab Key'")
        result = cursor.fetchone()
        
        status = result[0] if result else "Unknown"
        msg.body(f"The Main Lab Key is currently: {status}")
        conn.close()
    else:
        msg.body("Welcome to Digital Lab Assistant. Type 'Status' to check equipment.")

    return str(resp)

if __name__ == "__main__":
    with app.app_context():
        test_conn = get_db_connection()
        print("--- Database Connection Verified! ---")
        test_conn.close()
    app.run(port=5000)