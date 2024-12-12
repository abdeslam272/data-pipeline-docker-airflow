import psycopg2
import json

def load_to_db():
    with open("data/cleaned_data.json", "r") as file:
        data = json.load(file)

    conn = psycopg2.connect(
        dbname="airflow_db",
        user="airflow",
        password="airflow",
        host="localhost"
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            city TEXT,
            temperature FLOAT,
            humidity INT,
            weather TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO weather_data (city, temperature, humidity, weather)
        VALUES (%s, %s, %s, %s)
    """, (data["city"], data["temperature"], data["humidity"], data["weather"]))

    conn.commit()
    cursor.close()
    conn.close()

    print("Data loaded successfully.")
