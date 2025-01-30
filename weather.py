from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "Your own api key"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = {}

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi=no"

            # Fetch data from API
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather_data = {
                    "cityname": data["location"]["name"],
                    "country_code": data["location"]["country"],
                    "coordinate": f"{data['location']['lat']}, {data['location']['lon']}",
                    "temp": data["current"]["temp_c"],  # Temperature in Celsius
                    "pressure": data["current"]["pressure_mb"],  # Pressure in mb
                    "humidity": data["current"]["humidity"],
                    "condition": data["current"]["condition"]["text"],
                    "icon": data["current"]["condition"]["icon"]  # Weather icon
                }
            else:
                weather_data["error"] = "City not found. Please enter a valid city."

    return render_template("index.html", data=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
