import random
from datetime import date, timedelta
from database import get_connection
from dsa.linked_list import LinkedList
from dsa.merge_sort import merge_sort
from dsa.binary_search import binary_search

# Simulate and save 7 days of readings for a user
def simulate_usage(user_id):
    conn   = get_connection()
    cursor = conn.cursor()

    today = date.today()

    for i in range(7):
        day = today - timedelta(days=i)

        # Realistic Karachi ranges
        electricity = round(random.uniform(8,  35),  2)  # kWh
        water       = round(random.uniform(100, 400), 2)  # litres
        gas         = round(random.uniform(2,  15),  2)  # m³

        for utility, amount in [
            ("electricity", electricity),
            ("water",       water),
            ("gas",         gas)
        ]:
            # Check if record already exists for this day
            cursor.execute('''
                SELECT id FROM usage_data
                WHERE user_id=%s AND type=%s AND date=%s
            ''', (user_id, utility, day))

            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO usage_data (user_id, type, amount, date)
                    VALUES (%s, %s, %s, %s)
                ''', (user_id, utility, amount, day))

    conn.commit()
    conn.close()

# Load last 7 days into a Linked List
def get_usage_linked_list(user_id):
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date, type, amount
        FROM usage_data
        WHERE user_id = %s
        ORDER BY date DESC
        LIMIT 21
    ''', (user_id,))

    rows = cursor.fetchall()
    conn.close()

    # Build linked list from database records
    ll = LinkedList()
    for date_val, utility_type, amount in rows:
        ll.insert_at_front(str(date_val), utility_type, amount)

    return ll

# Get today's usage for all 3 utilities
def get_today_usage(user_id):
    conn   = get_connection()
    cursor = conn.cursor()

    today = date.today()

    result = {"electricity": 0, "water": 0, "gas": 0}

    cursor.execute('''
        SELECT type, amount FROM usage_data
        WHERE user_id = %s AND date = %s
    ''', (user_id, today))

    rows = cursor.fetchall()
    conn.close()

    for utility_type, amount in rows:
        result[utility_type] = amount

    return result

# Get last 7 days for one utility type (for Chart.js)
def get_chart_data(user_id, utility_type):
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date, amount FROM usage_data
        WHERE user_id = %s AND type = %s
        ORDER BY date ASC
        LIMIT 7
    ''', (user_id, utility_type))

    rows = cursor.fetchall()
    conn.close()

    labels  = [str(row[0]) for row in rows]
    amounts = [row[1]      for row in rows]

    return labels, amounts

# Get sorted history by amount (Merge Sort)
def get_sorted_usage(user_id):
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date, type, amount
        FROM usage_data
        WHERE user_id = %s
    ''', (user_id,))

    rows = cursor.fetchall()
    conn.close()

    records = []
    for date_val, utility_type, amount in rows:
        records.append({
            "date"         : str(date_val),
            "utility_type" : utility_type,
            "amount"       : amount
        })

    # Apply Merge Sort
    return merge_sort(records)

# Search by date (Binary Search)
def search_usage_by_date(user_id, target_date):
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date, type, amount
        FROM usage_data
        WHERE user_id = %s
    ''', (user_id,))

    rows = cursor.fetchall()
    conn.close()

    records = []
    for date_val, utility_type, amount in rows:
        records.append({
            "date"         : str(date_val),
            "utility_type" : utility_type,
            "amount"       : amount
        })

    # Apply Binary Search
    return binary_search(records, target_date)