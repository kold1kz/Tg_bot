import requests


weather_token='3ff4c81dc1c7cc9ab82543d10d685e8c'

city='Воронеж'


r=requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric"
            )
data=r.json()


temp_min = data["main"]["temp_min"]
temp_max=data["main"]["temp_max"]


print(data, '\n')
print('------------------------------------------')
print('\n')
print(temp_min, ':', temp_max)