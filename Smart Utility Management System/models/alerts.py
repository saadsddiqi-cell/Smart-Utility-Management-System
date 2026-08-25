from datetime import date
from database import get_connection
from dsa.priority_queue import MinHeap
from dsa.queue import Queue

# Check usage and generate alerts automatically
def generate_alerts(user_id, today_usage):
    conn   = get_connection()
    cursor = conn.cursor()

    alerts = []

    thresholds = {
        "electricity": {"limit": 30,  "unit": "kWh",    "priority": 1},
        "water"      : {"limit": 350, "unit": "Litres",  "priority": 2},
        "gas"        : {"limit": 12,  "unit": "m³",      "priority": 1},
    }

    today = date.today()

    for utility, config in thresholds.items():
        amount = today_usage.get(utility, 0)
        if amount > config["limit"]:
            message = (
                f"High {utility} usage detected! "
                f"You used {amount} {config['unit']} today "
                f"(limit: {config['limit']} {config['unit']})"
            )
            priority = config["priority"]

            # Check if alert already exists for today
            cursor.execute('''
                SELECT id FROM alerts
                WHERE user_id=%s AND message=%s AND date=%s
            ''', (user_id, message, today))

            if not cursor.fetchone():
                # Only insert if not already there
                cursor.execute('''
                    INSERT INTO alerts (user_id, message, priority, date)
                    VALUES (%s, %s, %s, %s)
                ''', (user_id, message, priority, today))
                alerts.append((priority, message))

    conn.commit()
    conn.close()
    return alerts


# Load alerts into Priority Queue
def get_alerts_priority_queue(user_id):
    conn   = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT message, priority, date
        FROM alerts
        WHERE user_id = %s
        ORDER BY date DESC
        LIMIT 10
    ''', (user_id,))

    rows = cursor.fetchall()
    conn.close()

    heap = MinHeap()
    for message, priority, date_val in rows:
        heap.insert(priority, {
            "message" : message,
            "priority": priority,
            "date"    : str(date_val)
        })

    return heap.to_list()


def check_email_sent_today(user_id):
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM alerts
        WHERE user_id = %s AND date = %s
    ''', (user_id, date.today()))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0