import requests, re, sys, os
from bs4 import BeautifulSoup

#Let users input the URL by themselves, and determine whether the URL is the specified list by regular expression, detect the error parameter by try/except, and save the URL by variable url.
while True:
    try:
        url = str(input('請輸入你要查詢天氣的網址（僅允許https://weather.com/），並且需切換至"10天"\n如果留空，預設為新北市永和區\n'))
        weatherurl = re.search('https://weather.com/', url)
        if url == '':
            #You can change the default URL by modifying the url variable below
            url = 'https://weather.com/zh-TW/weather/tenday/l/118b452e922d099a1b4857726e33e7d7cd8a7ff35be2ff3bab0fca9eaad7b4e7'
        elif weatherurl == None:
            raise ValueError
        break
    except ValueError:
        print('你輸入的網址有誤')
        print('')

print('')

#Let users input the number of days for the query, save the number of days by variable y, and check if the input value has decimal points or other disallowed conditions by try/except
while True:
    try:
        y = int(input('你要查詢幾天的天氣？（最低輸入1，最高輸入10）\n'))
        if y <=0:
            raise ValueError
        elif y >=11:
            raise ValueError
        break
    except ValueError:
        print('你輸入的數值有誤')
        print('')

#Create a header, visit the site, parse the data through Beautifulsoup, and store the data in a variable soup
headers = {'User-Agent': 'Chrome/66.0.3359.181'}
web = requests.get(url, headers=headers)
soup = BeautifulSoup(web.text, 'html.parser')

#Which area to get the weather information from
while True:
    try:
        locationname = str(soup.find('span', class_='LocationPageTitle--PresentationName--1AMA6').text).split(', ')
        break
    except AttributeError:
        print('無法在該網站查詢到任何資料')
        os.system('pause')
        sys.exit()

#When the data was last updated
timestamp = soup.find('div', class_='DailyForecast--timestamp--22Azh').text
finditertime = re.finditer(r'\d+', timestamp)
timestamp = []
for time in finditertime:
    timestamp.append(time.group())

print('')

#Output some basic information, such as region, data update time
print('查詢地區為：'+ locationname[1], locationname[0])
print('資料更新時間：'+ timestamp[0]+ ':'+ timestamp[1])

print('')

#----------Start getting weather-related values below----------

#Repeat the operation by looping, the number of executions is the variable y entered by the user
for i in range(y):
    detailIndex = 'detailIndex'+str(i)
    i = i + 1

    #Get local weather information
    #The variable dailycontent is used to get the whole day's weather information, save it and then break it down
    dailycontent = soup.find(id=detailIndex)

    #The variable datetime is used to capture the time and determine whether the first data is day or night
    #If the first data is night, the value of the variable datetime will be None
    datetime = dailycontent.find('h3', class_='DailyContent--daypartName--3emSU')
    datetime = re.search('白天', str(datetime))

    #The variable date is the date and day of the week of this data
    date = str(dailycontent.find('span', class_='DailyContent--daypartDate--3VGlz').text).split(' ')

    #The variable temperature is used to obtain the weather value for a day
    temperature = dailycontent.find_all('span', class_='DailyContent--temp--1s3a7')
    for z, x in enumerate(temperature):
        temperature[z] = x.text

    #The variable rain is used to obtain rainfall probability
    rain = dailycontent.find_all('span', attrs={'data-testid':'PercentageValue'}, class_='DailyContent--value--1Jers')
    for z, x in enumerate(rain):
        rain[z] = x.text

    #The variable humidity is used to obtain the moisture level
    humidity = dailycontent.find_all('span', attrs={'data-testid':'PercentageValue'}, class_='DetailsTable--value--2YD0-')
    for z, x in enumerate(humidity):
        humidity[z] = x.text

    #The variable uvindex is used to obtain the UV index
    uvindex = dailycontent.find_all('span', attrs={'data-testid':'UVIndexValue'}, class_='DetailsTable--value--2YD0-')
    for z, x in enumerate(uvindex):
        uvindex[z] = x.text

    #The variable sunrisetime is used to get the sunrise time
    sunrisetime = dailycontent.find_all('span', attrs={'data-testid':'SunriseTime'}, class_='DetailsTable--value--2YD0-')
    for z, x in enumerate(sunrisetime):
        sunrisetime[z] = x.text

    #The variable sunsettime is used to get the sunset time
    sunsettime = dailycontent.find_all('span', attrs={'data-testid':'SunsetTime'}, class_='DetailsTable--value--2YD0-')
    for z, x in enumerate(sunsettime):
        sunsettime[z] = x.text

    #print all data
    if datetime == None:
        print('----------'+ '\n'+ date[1]+ '號', date[0]+ '\n'+ '-----'+ '\n'+ '晚上'+ '\n'+ '    氣溫：'+ temperature[0]+ '\n'
    + '    降雨機率：'+ rain[0]+ '\n'+ '    濕度：'+ humidity[0]+ '\n'+ '    紫外線指數：'+ uvindex[0]+ '\n'+ '----------')
        print('')
    else:
        print('----------'+ '\n'+ date[1]+ '號', date[0]+ '\n'+ '-----'+ '\n'+ '早上'+ '\n'+ '    氣溫：'+ temperature[0]+ '\n'
        + '    降雨機率：'+ rain[0]+ '\n'+ '    濕度：'+ humidity[0]+ '\n'+ '    紫外線指數：'+ uvindex[0]+ '\n'+ '-----'+ '\n'+ '下午'
        + '\n'+ '    氣溫：'+ temperature[1]+ '\n'+ '    降雨機率：'+ rain[1]+ '\n'+ '    濕度：'+ humidity[1]+ '\n'
        + '    紫外線指數：'+ uvindex[1]+ '\n'+ '-----'+ '\n'+ '    日出時間：'+ sunrisetime[0]+ '\n'+ '    日落時間：'+ sunsettime[0]
        + '\n'+ '----------')
        print('')

#Pause the program to allow users to view messages
os.system('pause')