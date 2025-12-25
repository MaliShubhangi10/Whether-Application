import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

# ---------------- CONFIG ----------------
API_KEY = "Your_API_Key"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# ----------------------------------------


def get_weather():
    city = city_entry.get().strip()

    if not city or city == "Search city...":
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()

        if response.status_code != 200:
            messagebox.showerror("Error", data.get("message", "City not found").title())
            return

        temp = int(data["main"]["temp"])
        feels_like = int(data["main"]["feels_like"])
        weather = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        date_time = datetime.now().strftime("%A, %d %b %Y")

        condition = data["weather"][0]["main"].lower()
        icons = {
            "clear": "☀️",
            "clouds": "☁️",
            "rain": "🌧️",
            "snow": "❄️",
            "thunderstorm": "⛈️"
        }
        icon = icons.get(condition, "🌫️")

        city_label.config(text=city.title())
        date_label.config(text=date_time)
        temp_label.config(text=f"{temp}°C")
        icon_label.config(text=icon)
        desc_label.config(text=weather)
        info_label.config(
            text=f"Feels Like: {feels_like}°C\n"
                 f"Humidity: {humidity}%\n"
                 f"Wind: {wind} m/s"
        )

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error. Please try again.")


def clear_placeholder(event):
    if city_entry.get() == "Search city...":
        city_entry.delete(0, tk.END)


# ---------------- UI SETUP ----------------
root = tk.Tk()
root.title("Weather App")
root.geometry("380x560")
root.config(bg="#87CEEB")
root.resizable(False, False)
root.bind("<Return>", lambda event: get_weather())

# ---------------- SEARCH ----------------
search_frame = tk.Frame(root, bg="#87CEEB")
search_frame.pack(pady=20)

city_entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 13),
    width=22,
    justify="center",
    bg="white",
    fg="#2C3E50",
    bd=0
)
city_entry.pack(ipady=8)
city_entry.insert(0, "Search city...")
city_entry.bind("<FocusIn>", clear_placeholder)

search_btn = tk.Button(
    root,
    text="Get Weather",
    font=("Segoe UI", 11, "bold"),
    bg="#3498DB",
    fg="white",
    bd=0,
    width=16,
    cursor="hand2",
    command=get_weather
)
search_btn.pack(pady=12, ipady=6)

# ---------------- CARD ----------------
card = tk.Frame(root, bg="white")
card.pack(padx=20, pady=20, fill="both", expand=True)

city_label = tk.Label(
    card,
    text="City",
    font=("Segoe UI", 18, "bold"),
    bg="white",
    fg="#2C3E50"
)
city_label.pack(pady=(20, 5))

date_label = tk.Label(
    card,
    text="Date",
    font=("Segoe UI", 10),
    bg="white",
    fg="#7F8C8D"
)
date_label.pack()

icon_label = tk.Label(
    card,
    text="🌤️",
    font=("Segoe UI", 48),
    bg="white"
)
icon_label.pack(pady=10)

temp_label = tk.Label(
    card,
    text="--°C",
    font=("Segoe UI", 40, "bold"),
    bg="white",
    fg="#2C3E50"
)
temp_label.pack()

desc_label = tk.Label(
    card,
    text="Weather Condition",
    font=("Segoe UI", 14),
    bg="white",
    fg="#34495E"
)
desc_label.pack(pady=5)

info_label = tk.Label(
    card,
    text="Feels Like: --°C\nHumidity: --%\nWind: -- m/s",
    font=("Segoe UI", 12),
    bg="white",
    fg="#2980B9",
    justify="center"
)
info_label.pack(pady=20)

footer = tk.Label(
    root,
    text="Powered by OpenWeather API",
    font=("Segoe UI", 9),
    bg="#87CEEB",
    fg="#2C3E50"
)
footer.pack(pady=10)

root.mainloop()
