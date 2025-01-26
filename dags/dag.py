from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import requests
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.getenv("OPENWEATHER_API_KEY")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def fetch_and_store_forecast(**kwargs):
    """Fetches weather forecast data and stores it in PostgreSQL."""
    lat = kwargs.get('lat', 48.8566)  # Default: Paris latitude
    lon = kwargs.get('lon', 2.3522)  # Default: Paris longitude

    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        # Call the API
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_forecast (
            id SERIAL PRIMARY KEY,
            time TIMESTAMP NOT NULL,
            temperature NUMERIC NOT NULL,
            humidity NUMERIC NOT NULL,
            weather TEXT NOT NULL
        );
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = """
            INSERT INTO weather_forecast (time, temperature, humidity, weather)
            VALUES (%s, %s, %s, %s)
        """

        for forecast in data["list"]:
            time = forecast["dt_txt"]
            temp = forecast["main"]["temp"]
            humidity = forecast["main"]["humidity"]
            weather = forecast["weather"][0]["description"]

            cursor.execute(insert_query, (time, temp, humidity, weather))

        conn.commit()
        print("Weather data successfully inserted into PostgreSQL.")

    except requests.exceptions.RequestException as e:
        print(f"Error calling the API: {e}")
    except psycopg2.Error as e:
        print(f"PostgreSQL error: {e}")
    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'weather_forecast_dag',
    default_args=default_args,
    description='Fetch and store weather data in PostgreSQL',
    schedule_interval=timedelta(hours=1),  # Run every hour
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['weather', 'api', 'postgresql'],
) as dag:

    fetch_weather_task = PythonOperator(
        task_id='fetch_and_store_weather',
        python_callable=fetch_and_store_forecast,
        op_kwargs={'lat': 48.8566, 'lon': 2.3522},  # Coordinates for Paris
    )

    fetch_weather_task
