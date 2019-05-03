import speech_recognition as sr
import cv2
import sys
import subprocess
from subprocess import call
import pyttsx3
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font
import threading
import os


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

commands_list = ['start tracker', 'start notes']



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
                
            if 'quit' in speech:
                print('Quitting')
                engine.say('Quitting, goodbye')
                engine.runAndWait()
                time.sleep(0.5)
                window.destroy()
                break
            
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break

            if kill == True:
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

    
def quitFunction():
    print('quitting')
    window.destroy()
    os._exit(13)



window = tk.Tk()  
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
##window.geometry('1280x720')
buttonHeight = 10
buttonWidth = 35


font = font.Font(family='Helvetica', size=20, weight='bold')



n = ttk.Notebook(window)

f1 = ttk.Frame(n, width = window.winfo_screenwidth(), height = window.winfo_screenheight())
f2 = ttk.Frame(n, width = window.winfo_screenwidth(), height = window.winfo_screenheight())
n.add(f1, text='Dashboard')
n.add(f2, text='Voice Log')
n.grid()

f1.grid_propagate(False)
f2.grid_propagate(False)

voiceOutputBox = tk.Listbox(f2, height=20, width=33, font=font)
voiceOutputBox.place(x=500, y=50)

notesButton = tk.Button(f1, text ="Start Notes", font=font,command = startNotes, height = buttonHeight, width =buttonWidth )
notesButton.place(x=250, y=0)

trackerButton = tk.Button(f1, text ="Start Tracker", command = startTracker, height = buttonHeight, width =buttonWidth )
trackerButton.place(x=750, y=0)

quitButton= tk.Button(window, text ="quit", command = quitFunction, height = buttonHeight, width =buttonWidth )
quitButton.place(x=500,y=450)
  

window.mainloop()  

        

##key = cv2.waitKey(1) & 0xFF
##
##if key == ord('w'):
##    break
    
