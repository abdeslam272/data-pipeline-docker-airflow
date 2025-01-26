import os
import requests
import psycopg2
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

API_URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Clé API sécurisée
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def fetch_and_store_forecast(lat, lon):
    """Récupère les prévisions météorologiques et les insère dans PostgreSQL."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",  # Température en Celsius
    }

    try:
        # Appel à l'API
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Vérifier les erreurs HTTP
        data = response.json()

        # Connexion à PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        """Créer la table si elle n'existe pas déjà."""
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
        # Préparation des données et insertion dans la table
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

        conn.commit()  # Appliquer les changements
        print("Données insérées dans PostgreSQL avec succès.")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à l'API : {e}")
    except psycopg2.Error as e:
        print(f"Erreur PostgreSQL : {e}")
    finally:
        # Fermer la connexion à la base de données
        if conn:
            cursor.close()
            conn.close()

# Exemple : coordonnées pour Paris
if __name__ == "__main__":
    fetch_and_store_forecast(lat=48.8566, lon=2.3522)
