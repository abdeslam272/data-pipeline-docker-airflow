import json

def clean_and_transform():
    try:
        with open("data/raw_data.json", "r") as file:
            data = json.load(file)

        # Simplify data structure
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

    except FileNotFoundError:
        print("Error: raw_data.json file not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

clean_and_transform()
