import requests
from plyer import notification

CITY = "Вологда"
API_KEY = "23496c2a58b99648af590ee8a29c5348"
UNITS = "metric"
LANGUAGE = "en"

URL = fr"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANGUAGE}"

response = requests.get(URL)  #отправляем запрос и получили объект с данными
print(response.status_code)
print(response.json())


weather_dict = response.json() #temp, feels like, desc

temp = weather_dict["main"]["temp"]
tempFahrenheit = temp * 1.8 + 32
feels_like = weather_dict["main"]["feels_like"]
description = weather_dict["weather"][0]["description"]

print(f'The temperature is {temp} °C\n{tempFahrenheit} °F\nFeels like {feels_like} °C\nDescription: {description}')

notification.notify(
    title = "Weather",
    message = f'The temperature is {temp} °C\n{tempFahrenheit} °F\nFeels like {feels_like} °C\nDescription: {description}',
    timeout = 10
)