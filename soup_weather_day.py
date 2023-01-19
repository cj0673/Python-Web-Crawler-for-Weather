import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
url = 'https://weather.com/zh-TW/weather/today/l/25.0076143,121.5053019'
web = requests.get(url, headers=headers)
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