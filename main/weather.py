from bs4 import BeautifulSoup
from requests import get
import speech_recognition as sr
import pyttsx3
import time
import tkinter as tk
from tkinter import ttk, font, StringVar
import threading
import os
import subprocess

time.sleep(5)

r = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init()
engine.setProperty('rate', 150)


global window, voiceOutputBox, weatherLabel, tempLabel,w

def weather():

    while True:
        
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            speech = r.recognize_google(audio)
            print(speech)
            voiceOutputBox.insert(0, speech)

        except sr.UnknownValueError:
            print('could not understand speech, try again...')
            engine.say('could not understand, try again')
            time.sleep(1)
            engine.runAndWait()
            voiceOutputBox.insert(0, 'could not understand, try again')

        try: 
            if 'weather' in speech:
                

                url = 'https://weather.com/weather/today/l/ccb3317341d964ec4853607d78762743e9624022dfb117069ff2e7d45fb2a8e9'

                response = get(url)


                html_soup = BeautifulSoup(response.text, 'html.parser')

                tempElement = html_soup.find_all('div', class_ = 'today_nowcard-temp')
                temp = tempElement[0].span.text

                weatherElement = html_soup.find_all('div', class_ = 'today_nowcard-phrase')
                weather = weatherElement[0].text

                feelslikeElement = html_soup.find_all('div', class_ = 'today_nowcard-feels')
                feelslike = feelslikeElement[0].text



                print(temp, weather, feelslike)
                
                tempLabel.config(text='Temperature: '+temp)
                weatherLabel.config(text='Weather: '+weather)

                engine.say('The current temperature is' + temp)
                engine.say('It currently'+feelslike+'outside')

                engine.say('the weather is ' + weather)
                time.sleep(1)
                engine.runAndWait()
        
        except:
            print('didnt work')

        speech = None
            
t = threading.Thread(target=weather)
t.start()

window = tk.Tk()  
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
##window.geometry('1280x720')



font = font.Font(family='Helvetica', size=10, weight='bold')



n = ttk.Notebook(window)

f1 = ttk.Frame(n, width = 480, height = 320)
f2 = ttk.Frame(n, width = 480, height = 320)
n.add(f1, text='Weather')
n.add(f2, text='Voice Log')
n.grid()

f1.grid_propagate(False)
f2.grid_propagate(False)

voiceOutputBox = tk.Listbox(f2, height=20, width=25, font=font)
voiceOutputBox.pack()



weatherLabel = tk.Label(f1, height=5, width=20, text='Weather')
weatherLabel.place(x=175,y=100)


tempLabel = tk.Label(f1, height=5, width=20, text='Temperatrue')
tempLabel.place(x=175, y=0)

window.mainloop()





