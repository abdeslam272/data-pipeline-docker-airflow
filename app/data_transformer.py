import json

def clean_and_transform():
    with open("data/raw_data.json", "r") as file:
        data = json.load(file)

    # Exemple : simplifiez la structure des données
    cleaned_data = []
    for forecast in data["list"]:
        cleaned_data.append({
            "time": forecast["dt_txt"],
            "temperature": forecast["main"]["temp"],
            "humidity": forecast["main"]["humidity"],
            "weather": forecast["weather"][0]["description"],
        })

    with open("data/cleaned_data.json", "w") as file:
        json.dump(cleaned_data, file)

    print("Data transformed successfully.")
