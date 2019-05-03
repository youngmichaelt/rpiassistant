from gtts import gTTS
from pygame import mixer
import pyttsx3
import time
tts = gTTS(text='Tell me a command')
tts.save('response.mp3')
mixer.init()
mixer.music.load('response.mp3')
mixer.music.play()
time.sleep(4)
engine = pyttsx3.init()
engine.setProperty('voice','com.apple.speech.synthesis.voice.daniel')
engine.say('hi')
engine.runAndWait()
