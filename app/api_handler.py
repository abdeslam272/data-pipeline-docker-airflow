import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_URL = "https://api.openweathermap.org/data/2.5/forecast"
API_KEY = os.getenv("OPENWEATHER_API_KEY")  # Ensure the API key is loaded securely

def fetch_forecast(lat, lon):
    """Fetches weather forecast for the given coordinates."""
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",
        "lang": "en"
    }
    
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        print(f"Forecast for coordinates ({lat}, {lon}):")
        for forecast in data["list"]:  
            time = forecast["dt_txt"]
            temp = forecast["main"]["temp"]
            weather = forecast["weather"][0]["description"]
            print(f"{time} - Temp: {temp}°C, Weather: {weather.capitalize()}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
    except KeyError:
        print("Error: Unexpected response format. Please check the API response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage: Fetch forecast for Paris (coordinates)
fetch_forecast(lat=48.8566, lon=2.3522)
