import speech_recognition as sr
import sys
import subprocess
from subprocess import call

#initialize microphone
r = sr.Recognizer()
mic = sr.Microphone(device_index=2)

#main loop
while True:
    print('')
    print('What crytocurrency information would you like to hear')
    print('')
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        r.energy_threshold = 0.5

    try:
        speech = r.recognize_google(audio)
        print(speech)
        print('')

    except sr.UnknownValueError:
        print('could not understand')
