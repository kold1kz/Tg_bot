import datetime,requests
from config import weather_token
from aiogram.utils.helper import Helper, HelperMode, ListItem


class weather:
    def get_weather(city):
        code_smile={
                "Clear": "Ясно \U00002600",
                "Clouds": "Облачно \U00002601",
                "Rain": "Дождь \U00002614",
                "Drizzle": "Дождь \U00002614",
                "Thunderstorm": "Гроза \U000026A1",
                "Snow": "Снег \U0001F328",
                "Mist": "Туман \U0001F32B",
            }

        try:
            r=requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"
            )
            data=r.json()

            city=data["name"]
            cur_weather = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind=data["wind"]["speed"]
            sunrise=datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset=datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            time_day=datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            feels=data["main"]["feels_like"]

            wd=data["weather"][0]["main"]
            if wd in code_smile:
                wdd=code_smile[wd]
            else:
                wdd="Посмотри в окно, а то у меня нет глаз, не вижу что за погода!"

            return (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                f"Погода в городе: {city}\nТемпература: {cur_weather}C {wdd}\n"
                f"Ощущается как: {feels}C\n"
                f"Влажность: {humidity}%\nДавление: {pressure} mm.rt.ct\n"
                f"Ветер: {wind} m.s\nВосход: {sunrise}\nЗакат: {sunset}\n"
                f"Продолжительность дня: {time_day}\n"
                f"*** Наилучшего вам дня! ***")
        
        except:
            return ("\U00002620 Пожалуйста проверь написанние своего города \U00002620")

class TestStates(Helper):
    mode = HelperMode.snake_case

    TEST_STATE_0 = ListItem()
    TEST_STATE_1 = ListItem()
    TEST_STATE_2 = ListItem()
