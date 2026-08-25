import sys
sys.path.append('..')
from dsa.hash_table import HashTable
from database import get_connection

user_table = HashTable(size=50)

def load_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password, role FROM users")
    rows = cursor.fetchall()
    conn.close()
    for username, password, role in rows:
        user_table.insert(username, {
            "password": password,
            "role": role
        })
    print(f"Loaded {len(rows)} users into Hash Table")

def register_user(username, password, role="citizen", email="", phone=""):
    conn = get_connection()
    cursor = conn.cursor()

    if user_table.search(username):
        conn.close()
        return False, "Username already exists"

    try:
        cursor.execute(
            "INSERT INTO users (username, password, role, email, phone) VALUES (%s, %s, %s, %s, %s)",
            (username, password, role, email, phone)
        )
        conn.commit()
        conn.close()
        user_table.insert(username, {
            "password": password,
            "role": role
        })
        return True, "Registration successful"
    except Exception as e:
        conn.close()
        return False, str(e)

def login_user(username, password, selected_role="citizen"):
    user = user_table.search(username)
    if user is None:
        return False, "Username not found"
    if user["role"] != selected_role:
        return False, f"User is not registered as a {selected_role.capitalize()}."
    if user["password"] == password:
        return True, user["role"]
    else:
        return False, "Wrong password"