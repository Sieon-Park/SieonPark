import os
import tkinter as tk
from tkinter import messagebox

import requests


API_KEY = "YOUR_API_KEY"  # Replace with your actual OpenWeather API key
API_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather():
    city = entry_city.get().strip()

    if not city:
        label_result.config(text = "Type a city name.")
        return

    if not API_KEY:
        messagebox.showerror(
            "API Error",
            "OPENWEATHER_API_KEY environment variable is not set."
        )
        return

    try:
        response = requests.get(
            API_URL,
            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric",
                "lang": "kr",
            },
            timeout = 10,
        )
        response.raise_for_status()
        data = response.json()

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]

        label_result.config(
            text = (
                f"City: {data.get('name', city)}\n"
                f"Weather: {weather}\n"
                f"Temperature: {temp}°C\n"
                f"Feels Like: {feels_like}°C\n"
                f"Humidity: {humidity}%"
            )
        )

    except requests.exceptions.HTTPError as error:
        if response.status_code == 404:
            messagebox.showerror("Cannot Find City", "Check the city name and try again.")
        elif response.status_code == 401:
            messagebox.showerror("API Error", "Check your OpenWeather API key and try again.")
        else:
            messagebox.showerror("Error", f"The weather request failed.\n{error}")

    except requests.exceptions.RequestException as error:
        messagebox.showerror("Connection Error", f"Could not retrieve weather information.\n{error}")

    except (KeyError, IndexError, ValueError):
        messagebox.showerror("Response Error", "Could not read the weather data.")


root = tk.Tk()
root.title("Weather Checker")
root.geometry("800x600")

label_title = tk.Label(
    root,
    text = "Enter a city name",
    font = ("Arial", 30)
)
label_title.pack(pady=(50, 20))

entry_city = tk.Entry(root, font = ("Arial", 15))
entry_city.pack()
entry_city.insert(0, "Seoul")

button_search = tk.Button(
    root,
    text = "Check Weather",
    command = get_weather
)
button_search.pack(pady = 50)

label_result = tk.Label(
    root,
    text = "",
    font = ("Arial", 15),
    justify = "left"
)
label_result.pack(pady = 15)

root.mainloop()