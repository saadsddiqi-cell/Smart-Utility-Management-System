import pymysql

def get_connection():
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
        database="smart_utility"
    )
    return conn

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL,
                role VARCHAR(20) NOT NULL
            )
        ''')

        # Usage table (electricity, water, gas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                type VARCHAR(20) NOT NULL,
                amount FLOAT NOT NULL,
                date DATE NOT NULL
            )
        ''')

        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                message VARCHAR(255) NOT NULL,
                priority INT NOT NULL,
                date DATE NOT NULL
            )
        ''')

        # Areas table (electricity + water + gas)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS areas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                area_name VARCHAR(100) NOT NULL,
                electricity_load FLOAT NOT NULL,
                water_level FLOAT NOT NULL,
                gas_pressure FLOAT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
        print("Database initialized successfully!")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    init_db()