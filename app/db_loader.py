import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "my_database")
DB_USER = os.getenv("DB_USER", "my_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "my_password")

# Attempt to connect to the database
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    print("Successfully connected to PostgreSQL")

    # Example database operation, e.g., creating a table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
        time TIMESTAMP,
        temperature FLOAT,
        humidity INT,
        weather VARCHAR(255)
    )
    """)
    conn.commit()
    
    cursor.close()
    conn.close()
except Exception as e:
    print("Error connecting to PostgreSQL:", e)
