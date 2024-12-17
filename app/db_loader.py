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
            time TIMESTAMP,
            temperature FLOAT,
            humidity INT,
            weather TEXT
        )
    """)

    # Insérer chaque enregistrement de la donnée transformée
    for entry in data:
        cursor.execute("""
            INSERT INTO weather_data (time, temperature, humidity, weather)
            VALUES (%s, %s, %s, %s)
        """, (entry["time"], entry["temperature"], entry["humidity"], entry["weather"]))

    conn.commit()
    cursor.close()
    conn.close()

    print("Data loaded successfully.")
