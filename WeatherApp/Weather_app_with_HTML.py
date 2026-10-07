import os

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
API_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."
        elif not API_KEY:
            error = "Please set your OpenWeather API key."
        else:
            try:
                response = requests.get(
                    API_URL,
                    params={
                        "q": city,
                        "appid": API_KEY,
                        "units": "metric",
                        "lang": "en",
                    },
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()

                weather = {
                    "city": data.get("name", city),
                    "description": data["weather"][0]["description"],
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                }

            except requests.exceptions.HTTPError:
                if response.status_code == 404:
                    error = "City not found. Please check the spelling and try again."
                elif response.status_code == 401:
                    error = "Invalid or inactive API key. Please check your OpenWeather API key."
                else:
                    error = f"Weather request failed with status code {response.status_code}."

            except requests.exceptions.RequestException:
                error = "Could not retrieve weather information. Please check your internet connection."

    return render_template(
        "index.html",
        weather=weather,
        error=error,
        city=city,
    )


if __name__ == "__main__":
    app.run(debug=True)
