import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "votre_api_key"  # Inscrivez-vous pour une clé API gratuite

def fetch_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"Weather in {city}:")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Humidity: {data['main']['humidity']}%")
    else:
        print(f"Error: {response.status_code}, {response.text}")

fetch_weather("Paris")
