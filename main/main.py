import speech_recognition as sr
import cv2
import sys
import subprocess
from subprocess import call

r = sr.Recognizer()
mic = sr.Microphone(device_index=2)
i = 0
speech = None
tracker = False
notes = True

while True:
    
    print('speak')
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        r.energy_threshold = 0.5

    try:
        speech = r.recognize_google(audio)
        print(speech)

    except sr.UnknownValueError:
        print('could not understand')
##        follow = [sys.executable, 'trackwmotion.py']
##        subprocess.call(follow)
##        if tracker == False:
##            
##            p = subprocess.Popen(['python', 'trackwmotion.py'])
####            q = subprocess.Popen(['python', 'test.py'])
##            tracker = True
##        


    if speech is not None:
        
        if 'start tracker' in speech and tracker == False:
            
        #start tracker
            print('Starting Tracker')
            p = subprocess.Popen(['python', 'trackwmotion.py'])
            tracker = True           

        if 'stop tracker' in speech and tracker == True:
            
            print('Stopping Tracker')
            p.terminate()
            tracker = False
        if 'start notes' in speech and notes == True:
            
            print('opening notes')
            p = subprocess.Popen(['python', 'notes.py'])
            break
            
        



        

    key = cv2.waitKey(1) & 0xFF

    if key == ord('w'):
        break
    
