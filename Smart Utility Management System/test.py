import pymysql

try:
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="smart_utility"
    )
    print("Connected!")
    conn.close()
except Exception as e:
    print("Error:", e)