import requests
from tkinter import *
import time
import datetime as dt
# from grap import getPlot
# from PIL import Image, ImageTk

apiKey = 'your api key here'
cashWeather = None
timeWeather = 100.0

s_city = "Ekaterinburg"
city_id = 0
appid = apiKey

def getCity():
    # try:
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                 params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
    data = res.json()
    print(data['cod'],data['message'])
    # print(data)
    cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in data['list']]
    print("city:", cities)

    city_id = data['list'][0]['id']
    print('city_id=', city_id)
    #except Exception as e:
    #     print("Exception (find):", e)
    #     pass

# city: ['Sevastopol (UA)']
# city_id= 694423
# city: ['Yekaterinburg (RU)']
# city_id= 1486209

def getweather(city_id):
    global cashWeather
    global timeWeather
    currTime = time.time()
    if currTime-timeWeather > 120 or cashWeather is None:
        cashWeather = getweatherAPI(city_id)
        timeWeather = currTime
        print('weather has updated frm API')
        return cashWeather
    else:
        return cashWeather


def getweatherAPI(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        # print("conditions:", data['weather'][0]['description'])
        # print("temp:", data['main']['temp'])
        # print(data)
        return data  # data['main']['temp'],data['weather'][0]['description']
    except Exception as e:
        print("Exception (weather):", e)
        return None


def getforeca(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid,'exclude':'daily'})
        data = res.json()
        for i in data['list']:
            print(i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'])
    except Exception as e:
        print("Exception (forecast):", e)
        pass
def getDescWind(degree):
    if (degree>337.5): return 'North'
    if (degree>292.5): return 'North West'
    if(degree>247.5): return 'West'
    if(degree>202.5): return 'South West'
    if(degree>157.5): return 'South'
    if(degree>122.5): return 'South East'
    if(degree>67.5): return 'East'
    if(degree>22.5): return 'North East';
    return 'North';

if __name__ == '__main__':
    window = Tk()
    window.title("Погода")
    c = Canvas(window, width=1000, height=750, bg='black')
    c.pack()
    placeT = c.create_text(390, 20, text='Город', fill="gray", font=('Arial',35))
    tT = c.create_text(390, 150, text='temp °', fill="white", font=('Arial', 160))
    conT = c.create_text(390, 280, text='описание', fill="gray", font=('Arial', 45))
    windT = c.create_text(390, 350, text='wind' + ' m/s,   ' + ' dir', fill="gray", font=('Arial', 25))
    progressT = c.create_rectangle(10, 10, 30, 10 + 200, fill='#333333')

    # getPlot(['0'], [0], [0])
    # workPath = '/dev/shm/foreca/weath.png'
    # pilImage = Image.open(workPath)
    # image = ImageTk.PhotoImage(pilImage)
    # imageT = c.create_image(400, 550, image=image)

    restoredDict ={}
    timeOut = 150
    last = timeOut
    while True:
        data = getweather(1486209)
        if data is None:
            print('no rezult of req. pause 100')
            time.sleep(100)
            continue
        t = data['main']['temp']
        con = data['weather'][0]['description']
        wind = data['wind']['speed']
        winddeg = data['wind']['deg']
        winddesc = getDescWind(winddeg)
        place = data['name']
        pressure = data['main']['pressure']

        c.itemconfig(placeT,text=place)
        c.itemconfig(tT,text=str(t)+'°')
        c.itemconfig(conT,text=con)
        c.itemconfig(windT,text=str(wind)+' m/s,   '+winddesc)

        tstam = time.time()
        curr = dt.datetime.fromtimestamp(tstam)
        currH = '%s:00' % (str(curr.hour).zfill(2))
        if len(restoredDict)>22:
            del restoredDict[list(restoredDict.keys())[0]]
        restoredDict[currH] = {'temp':t,'pressure':pressure}
        # x = list(restoredDict.keys())
        # y = [restoredDict[xx]['temp'] for xx in x]
        # y2= [restoredDict[xx]['pressure'] for xx in x]
        # getPlot(x, y, y2)
        # workPath = '/dev/shm/foreca/weath.png'
        # pilImage = Image.open(workPath)
        # image = ImageTk.PhotoImage(pilImage)
        # c.itemconfig(imageT,imaege=image)
        window.update()

        while last>0:
            last -=1
            c.coords(progressT, 10, 10, 30, 10 + int(200 * last/timeOut))
            window.update()
            time.sleep(1)

        last = timeOut
        window.update()


    # getforeca(1486209)

    window.mainloop()