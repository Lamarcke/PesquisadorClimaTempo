from tkinter import *
import requests
import os
import urllib.request
from PIL import ImageTk, Image

main = Tk()

def get_icons():
    script_run = './data/opened.dat'
    if not os.path.isfile(script_run):
        print("Iniciando download de icones...\nIsso pode levar alguns segundos...")
        icon_day = ['01d.png', '02d.png', '03d.png', '04d.png', '09d.png', '10d.png', '11d.png', '13n.png', '50d.png']
        icon_night = ['01n.png', '02n.png', '03n.png', '04n.png', '09n.png', '10n.png', '11n.png', '13n.png', '50n.png']
        img_dir = './data/img/'
        img_url = 'https://openweathermap.org/img/w/'
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        for name in icon_day:
            file_name = img_dir + name
            if not os.path.exists(file_name):
                urllib.request.urlretrieve(img_url + name, file_name)
        for name in icon_night:
            file_name = img_dir + name
            if not os.path.exists(file_name):
                urllib.request.urlretrieve(img_url + name, file_name)
        script_file = open(script_run, 'w+')
        script_file.close()
        print("Captura de icones realizada com sucesso.")
    else:
        return


def format_weather(weather):
    # noinspection PyGlobalUndefined
    global iconfile
    # noinspection PyGlobalUndefined
    global weathericon_file
    try:
        print("Resolvendo valores...")
        icon = weather['weather'][0]['icon'] + '.png'
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
        temp_max = weather['main']['temp_max']
        temp_min = weather['main']['temp_min']
        final_str = f"Cidade: {name}\nTemperatura: {int(temp)}\nTemperatura MAX: {int(temp_max)}\n" \
                    f"Temperatura MIN: {int(temp_min)}"
        print(f'Informações obtidas: \n{final_str}')
        iconfile = Image.open(f'./data/img/{icon}')
        iconfile = iconfile.resize((100, 80), Image.ANTIALIAS)
        weathericon_file = ImageTk.PhotoImage(iconfile)
        weathericon.create_image(45, 30, image=weathericon_file)
        weathercondition['text'] = desc

    except KeyError:
        final_str = 'Valor inserido inválido, por favor, verifique a ortografia.'
    except TimeoutError:
        final_str = 'Erro ao tentar receber as informações do servidor, por favor, tente novamente.'
    except ConnectionAbortedError:
        final_str = 'Erro ao tentar receber as informações do servidor, por favor, tente novamente.'
    except ConnectionResetError:
        final_str = 'Erro ao tentar receber as informações do servidor, por favor, tente novamente.'
    except ConnectionRefusedError:
        final_str = 'Erro ao tentar receber as informações do servidor, por favor, tente novamente.'
    except ConnectionError:
        final_str = 'Erro ao tentar receber as informações do servidor, por favor, tente novamente.'

    return final_str


def get_weather(city):
    print("Conectando a API OpenWeather...")
    weather_key = 'OPENWEATHER_API'
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {'APPID': weather_key, 'q': city + weather_country, 'units': 'metric'}
    weather_response = requests.get(weather_url, params=weather_params)
    weather = weather_response.json()
    weatherinfo['text'] = f"\n{format_weather(weather)}"


get_icons()
# Minimalistic Landscape Wallpaper by ZacTheAcorn
background_image = PhotoImage(file='./data/img/landscape.png')
background_render = Label(main, image=background_image)
background_render.place(relwidth=1, relheight=1)
tempsystem = 'ºC'
country = 'Brasil'
weather_country = ',br'
upper_frame = Frame(main, bg='#44d2fc', bd='5')
upper_frame.place(relx=0.5, rely=0.12, relwidth=0.73, relheight=0.15, anchor='n')
cityname = Entry(upper_frame, font=35)
cityname.place(relwidth=0.75, relheight=0.7)
cityname.focus_set()
countryname = Label(upper_frame, text=f'País Atual: {country}', bg='#44d2fc', )
countryname.place(relx=0, rely=0.8)
tempsimbol = Label(upper_frame, text=f'Temperatura em: {tempsystem}', bg='#44d2fc', )
tempsimbol.place(relx=0.37, rely=0.8)
searchbt = Button(upper_frame, text='Pesquisar', font=('Courier', 12), command=lambda: get_weather(cityname.get()))
searchbt.place(relx=0.77, rely=0, relwidth=0.23, relheight=1)

lower_frame = Frame(main, bg='#44d2fc', bd='8')
lower_frame.place(relx=0.5, rely=0.30, relwidth=0.73, relheight=0.6, anchor='n')
weatherinfo = Label(lower_frame, font=('Courier', 16), justify='center', anchor='n')
weatherinfo.place(relwidth=1, relheight=1)
weathericon = Canvas(lower_frame)
weathericon.place(relx=0.40, rely=0.6, relwidth=0.6, relheight=0.35)
weathercondition = Label(lower_frame, anchor='n')
weathercondition.place(relx=0.4, rely=0.75)

main.geometry("600x500+500+200")
main.title("SimpleWeather")
main.iconbitmap('./data/img/sun.ico')
main.resizable()
main.mainloop()
