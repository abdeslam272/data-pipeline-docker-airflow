import json

def clean_and_transform():
    with open("data/raw_data.json", "r") as file:
        data = json.load(file)

    # Exemple : simplifiez la structure des données
    cleaned_data = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
    }

    with open("data/cleaned_data.json", "w") as file:
        json.dump(cleaned_data, file)

    print("Data transformed successfully.")
