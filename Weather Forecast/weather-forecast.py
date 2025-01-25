import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tkb
import datetime 

def get_weather(city):
    API_key = "0632003198e69df7db6a3a85bb3cfa59"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code ==404:
        messagebox.showerror("Error", "City not found")
        return None

    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temp = weather['main']['temp'] - 273.15
    desc = weather['weather'][0]['description']
    humidity = weather['main']['humidity']
    windspeed = weather['wind']['speed']
    city = weather['name']
    country = weather['sys']['country']
    timezone_offset = weather['timezone']
    utc_time = datetime.datetime.now(datetime.timezone.utc)
    local_time = utc_time + datetime.timedelta(seconds=timezone_offset)
    date_time = local_time.strftime("%b %d, %I:%M %p")

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temp, desc, humidity, windspeed, city, country, date_time)


def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    icon_url, temp, desc, humidity, windspeed, city, country, date_time = result

    loc_label.configure(text=f"{city}, {country}")
    date_time_label.configure(text=f"{date_time}")

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    temp_label.configure(text=f"{temp:.0f}°C")
    desc_label.configure(text=f"{desc.title()}")
    humidity_label.configure(text=f"Humidity: {humidity}%")
    wind_label.configure(text=f"Wind Speed: {windspeed}m/s")


root = tkb.Window(themename="solar")
root.title("Weather Forecast")
root.geometry("600x520")

city_entry =tkb.Entry(root, font="Montserrat, 14")
city_entry.pack(pady=(20,10), padx=20)

btnSearch = tkb.Button(root, text = "Search", command = search, bootstyle = "primary")
btnSearch.pack(pady=10)

date_time_label = tkb.Label(root, font="Montserrat, 12", bootstyle="secondary")
date_time_label.pack(pady=(20,0))

loc_label = tkb.Label(root, font="Montserrat, 25", bootstyle="success")
loc_label.pack()

icon_label = tkb.Label(root)
icon_label.pack()

temp_label = tkb.Label(root, font=("Montserrat", 18, 'bold'), bootstyle="primary")
temp_label.pack()

desc_label = tkb.Label(root, font=("Montserrat", 16, 'bold'), bootstyle="primary")
desc_label.pack(pady=(0,10))

humidity_label = tkb.Label(root, font="Montserrat, 13", bootstyle="secondary")
humidity_label.pack()

wind_label = tkb.Label(root, font="Montserrat, 13", bootstyle="secondary")
wind_label.pack(pady=(0,20))

root.mainloop()