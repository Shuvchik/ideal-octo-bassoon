import requests
import json
import csv
from pathlib import Path

API_KEY = '728bfd79ce0ff19246ef168051542835'
city_id=524901

# Функция собирает данные от https://home.openweathermap.org/api по городам, записывает в словарь
def get_weather_by_cities():
    # получение данных от https://home.openweathermap.org/api

    cities = ['Moscow', 'Kursk', 'Tula', 'Voronezh', 'Yaroslavl', 'Lipetsk', 'Volgograd', 'Vladimir', 'Kazan', 'Penza',
              'Smolensk', 'Novosibirsk', 'Surgut', 'Magadan', 'Kurgan', 'Norilsk']
    weather = {}
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/find?q={city},RU&type=like&APPID={API_KEY}'
        response = requests.get(url)
        data = response.json()['list'][0]['main']['temp'] - 273.15
        weather[city] = round(data, 1)
    # print(weather[0])
    print(type(weather))
    print(weather)
    return weather

# Функция собирает данные от https://home.openweathermap.org/api по Москве за 5 дней, записывает в словарь
def get_weather_in_moscow():
    weather_in_moscow = {}
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': {API_KEY}})
        data = res.json()
        for i in data['list']:
            weather_in_moscow[i['dt_txt']] = i['main']['temp']
    except Exception as e:
        print("Exception (forecast):", e)
    print(f'weather_in_moscow {type(weather_in_moscow)}')
    print(weather_in_moscow)
    return weather_in_moscow

#Функция записывает данные в файл .csv
def to_csv(path: Path, data, name) -> None:
    result = []
    for key, temp in data.items():
        result.append({name: key, 'temp': float(temp)})
    with open(path, 'w', encoding='UTF-8', newline='') as csv_write:
        csv_write = csv.DictWriter(csv_write, fieldnames=[name, 'temp'], dialect='excel', quoting=csv.QUOTE_ALL)
        csv_write.writeheader()
        csv_write.writerows(result)

if __name__ == '__main__':
    weather = get_weather_by_cities()
    weather_in_moscow = get_weather_in_moscow()
    to_csv(Path('weather.csv'), weather, 'city')
    to_csv(Path('weather_moscow.csv'), weather_in_moscow, 'datetimes')

