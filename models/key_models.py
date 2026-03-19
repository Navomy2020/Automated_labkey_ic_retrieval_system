import mysql.connector
from database_config import get_db_connection

def get_all_lab_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT lab_name FROM labs")
    labs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return labs

def get_currently_issued_labs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT lab_name FROM labs WHERE status != 'Available'")
    labs = [row[0] for row in cursor.fetchall()]
    conn.close()
    return labs

def get_lab_status_details(lab_name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT l.lab_name, l.status, u.name as holder_name, u.phone as holder_phone, u.id as holder_id
        FROM labs l
        LEFT JOIN users u ON l.current_holder_id = u.id
        WHERE l.lab_name = %s
    """
    cursor.execute(query, (lab_name,))
    result = cursor.fetchone()
    conn.close()
    return result if result else {"error": "Lab not found"}

def approve_transfer_in_db(requester_phone, lab_name):
    """Directly updates the database holder when the user confirms receipt."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Get the ID of the person who is now taking the key
        cursor.execute("SELECT id FROM users WHERE phone = %s", (requester_phone,))
        user = cursor.fetchone()
        
        if user:
            # 2. Update the labs table to set this person as the new holder
            update_query = "UPDATE labs SET current_holder_id = %s, status = 'Issued' WHERE lab_name = %s"
            cursor.execute(update_query, (user['id'], lab_name))
            conn.commit()
            return True
    except Exception as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()
    return False