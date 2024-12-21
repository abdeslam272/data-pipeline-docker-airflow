import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL")

    # Create table if not exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        time TIMESTAMP,
        temperature FLOAT,
        humidity INT,
        weather VARCHAR(255)
    )
    """)
    conn.commit()

    # Insert sample data (or actual API data later)
    cursor.execute("""
    INSERT INTO weather_data (time, temperature, humidity, weather)
    VALUES (NOW(), 25.3, 60, 'Sunny')
    """)
    conn.commit()

    print("Data inserted successfully")
    cursor.close()
    conn.close()
except Exception as e:
    print("Error:", e)
