import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Chrome/66.0.3359.181'}
web = requests.get("https://weather.com/zh-TW/weather/today/l/53c5c38d4c75c225b874f434b19862ba5ab939e4e87866a0aa20eccf0e31233f", headers=headers)

soup = BeautifulSoup(web.text, 'html.parser')
weather = soup.select('span.CurrentConditions--timestamp--1ybTk')
for a in weather:
    b = a.text
    b = b.split(' ')
    print('上次更新時間 ： ' + b[1])

weather = soup.select('div.CurrentConditions--body--l_4-Z span.CurrentConditions--tempValue--MHmYY')
for a in weather:
    print('目前氣溫 ： ' + a.text)

weather = soup.select('ul.WeatherTable--columns--6JrVO.WeatherTable--wide--KY3eP li.Column--active--27U5T span.Column--precip--3JCDO')
for a in weather:
    b = a.text
    b = b.split('降雨機率')
    print('降雨機率 ： ' + b[1])