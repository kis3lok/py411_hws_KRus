import requests
from plyer import notification

CITY = "Вологда"
API_KEY = "23496c2a58b99648af590ee8a29c5348"
UNITS = "metric"
LANGUAGE = "en"

URL = fr"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units={UNITS}&lang={LANGUAGE}"

