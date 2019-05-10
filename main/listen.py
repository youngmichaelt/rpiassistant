import speech_recognition as sr
import sys
import os
import time
import pyttsx3
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

time.sleep(5)

r = sr.Recognizer()
mic = sr.Microphone(device_index=2)
print(mic)
engine = pyttsx3.init()

global window, voiceOutputBox

def listenMain():

    while True:

        with mic as source:
            print(source)
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            speech = r.recognize_google(audio)
            print(speech)
            voiceOutputBox.insert(0, speech)

        except sr.UnknownValueError:
            print('Say "Hey Marvin" if you want to get my attention')
            voiceOutputBox.insert(0, 'didnt understand')



        try:
            if 'Marvin' in speech:
                engine.say('hello')
                time.sleep(1)
                engine.runAndWait()

                p = subprocess.Popen(['python', 'main.py'])
                os._exit(13)
                window.destroy()
                
        except:
            print('failed')


            
t = threading.Thread(target=listenMain)
t.start()

window = tk.Tk()
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

n = ttk.Notebook(window)

f1 = ttk.Frame(n, width = window.winfo_screenwidth(), height = window.winfo_screenheight())
f2 = ttk.Frame(n, width = window.winfo_screenwidth(), height = window.winfo_screenheight())
n.add(f1, text='Dashboard')
n.add(f2, text='Voice Log')
n.grid()

f1.grid_propagate(False)
f2.grid_propagate(False)

voiceOutputBox = tk.Listbox(f2, height=20, width=33)
voiceOutputBox.pack()


label = tk.Label(f1, text='Say Hey Marvin to start',height=20, width=20)
label.pack()


window.mainloop()

                
