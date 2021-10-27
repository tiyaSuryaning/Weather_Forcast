from tkinter import *
from configparser import ConfigParser
import requests
from tkinter import messagebox

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # tuple cointains {City, Country, temp_celsius, temp_fahrenheit, icon, weather}
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_celsius * (9/5)) + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city, country, temp_celsius, temp_fahrenheit, icon, weather)
        return final
    else:
        return None

def search():
    city = city_name.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{}, {}'.format(weather[0], weather[1])
        #image['bitmap'] = 'weather_icons/{}.png'.format(weather[4])
        img["file"] = 'weather_icons\\{}.png'.format(weather[4])
        temp_lbl['text'] = '{:.2f}C, {:.2f}F'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[5]
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))

app = Tk()
app.title('Weather Forcast')
app.geometry('300x250')
#app.configure(background='gray')

city_name = StringVar()
city_name = Entry(app, textvariable=city_name)
city_name.pack()

search_btn = Button(app, text='This city', width=12, command=search)
search_btn.pack()

location_lbl = Label(app, text="", font=('bold', 20))
location_lbl.pack()

img = PhotoImage(file ="")
Image = Label(app, image=img)
Image.pack()

temp_lbl = Label(app, text='')
temp_lbl.pack()

weather_lbl = Label(app, text='')
weather_lbl.pack()

app.mainloop()