import speech_recognition as sr
import cv2
import sys
import subprocess
from subprocess import call
import pyttsx3
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font, Canvas, Scrollbar, Frame
import threading
import os
from requests import get
from bs4 import BeautifulSoup

time.sleep(5)
#initialize microphone
r = sr.Recognizer()
mic = sr.Microphone(device_index=2)
#init voice
engine = pyttsx3.init()
engine.setProperty('voice','com.apple.speech.synthesis.voice.daniel')


#initialize variables
i = 0
speech = None
tracker_on = False
notes_on = False

conversation = 0

commands_list = ['start tracker', 'start notes', 'start weather']



global window
global voiceOutputBox

#main loop
def main_loop():
    i = 0
    speech = None
    
    notes_on = False

    conversation = 0

    commands_list = ['start tracker', 'start notes']
    while True:

        if conversation == 0:
            print('')
            print('Tell me a command')
            print('')
            engine.say('Tell me a command')
            engine.runAndWait()
            time.sleep(1)
            conversation += 1
            
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
    ##        r.energy_threshold = 0.5

        try:
            speech = r.recognize_google(audio)
            print(speech)
            print('')
            voiceOutputBox.insert(0, speech)
            
            

        except sr.UnknownValueError:
            print('could not understand')
            engine.say('I cannot understand you, please try again')
            engine.runAndWait()
            time.sleep(1)
            voiceOutputBox.insert(0, 'could not understand')

        except KeyboardInterrupt:
            print('key')
            sys.exit()
            
            
    


        if speech is not None:

            #list commands
            if 'list commands' in speech:
                print('Listing Commands')
                print('')
                engine.say('Okay, listing commands')
                engine.runAndWait()
                time.sleep(1)
                for command in commands_list:
                    print(command)
                    engine.say(command)
                    engine.runAndWait()
                    time.sleep(0.5)
                    
                conversation = 0   
                
            #start tracker
            if 'start tracker' in speech and tracker_on == False:
                print('Starting Tracker')
                print('')
                engine.say('Okay, starting tracker')
                engine.runAndWait()
                time.sleep(0.5)
                p = subprocess.Popen(['python', 'trackwmotion.py'])
                window.destroy()
                break
            
            #stop tracker
##            if 'stop tracker' in speech and tracker_on == True:
##                print('Stopping Tracker')
##                print('')
##                engine.say('Stopping tracker')
##                engine.runAndWait()
##                time.sleep(0.5)
##                p.terminate()
##                tracker = False
##                conversation = 0 

            #start notes    
            if 'start notes' in speech and notes_on == False:
                print('Opening Notes App')
                engine.say('Okay, starting notes app')
                engine.runAndWait()
                time.sleep(0.5)
                p = subprocess.Popen(['python', 'notes.py'])
                window.destroy()
                break

            if 'start weather' in speech:
                print('Opening Weather')
                engine.say('Okay, starting weather')
                engine.runAndWait()
                time.sleep(0.5)
                p = subprocess.Popen(['python', 'weather.py'])
                window.destroy()
                break

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
                
                
                engine.say('The current temperature is' + temp)
                engine.say('It currently'+feelslike+'outside')

                engine.say('the weather is ' + weather)
                time.sleep(1)
                engine.runAndWait()
                

            
                
            if 'quit' in speech:
                print('Quitting')
                engine.say('Quitting, goodbye')
                engine.runAndWait()
                time.sleep(0.5)
                break
                p = subprocess.Popen(['python', 'listen.py'])
                window.destroy()
                break
            
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

            
            


    
    
    


t = threading.Thread(target=main_loop)

t.daemon=True

t.start()

def startNotes():
    
    p = subprocess.Popen(['python', 'notes.py'])
    window.destroy()
    print('trying to kill thread')
    os._exit(13)

def startTracker():
    
    p = subprocess.Popen(['python', 'trackwmotion.py'])
    window.destroy()
    print('trying to kill thread')
    os._exit(13)

def startWeather():
    p = subprocess.Popen(['python', 'weather.py'])
    window.destroy()
    os._exit(13)

def startManualMovement():
    p = subprocess.Popen(['python', 'manualmovement.py'])
    window.destroy()
    os._exit(13)

    
def quitFunction():
    print('quitting')
    
    window.destroy()
    p = subprocess.Popen(['python', 'listen.py'])
    os._exit(13)



window = tk.Tk()  
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
##window.geometry('480x320')
buttonHeight = 5
buttonWidth = 15


font = font.Font(family='Helvetica', size=10, weight='bold')

n = ttk.Notebook(window)



f1 = ttk.Frame(n, width = 480, height = 320)
f2 = ttk.Frame(n, width = 480, height = 320)
n.add(f1, text='Dashboard')
n.add(f2, text='Voice Log')
n.grid()

f1.grid_propagate(False)
f2.grid_propagate(False)



voiceOutputBox = tk.Listbox(f2, height=10, width=40, font=font)
voiceOutputBox.place(x=35, y=20)

notesButton = tk.Button(f1, text ="Notes",command = startNotes, height = buttonHeight, width =buttonWidth )
notesButton.place(x=0, y=0)

trackerButton = tk.Button(f1, text ="Tracker", command = startTracker, height = buttonHeight, width =buttonWidth )
trackerButton.place(x=160, y=0)

manualButton = tk.Button(f1, text ="Manual Movement", command = startManualMovement, height = buttonHeight, width =buttonWidth )
manualButton.place(x=320, y=0)

weatherButton = tk.Button(f1, text = "Weather", command = startWeather, height=buttonHeight, width = buttonWidth)
weatherButton.place(x = 0, y = 100)



quitButton= tk.Button(window, text ="quit", command = quitFunction, height = 3, width =8)
quitButton.place(x=375,y=200)
  

window.mainloop()  

        

##key = cv2.waitKey(1) & 0xFF
##
##if key == ord('w'):
##    break
    
