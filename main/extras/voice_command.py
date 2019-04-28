import speech_recognition as sr
import cv2
r = sr.Recognizer()
mic = sr.Microphone(device_index=2)
i = 0

while i < 10:
    print(mic)
    print('speak')
    print(sr.Microphone.list_microphone_names())
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
##        r.energy_threshold = 0.5
        print(mic)

    try:
        speech = r.recognize_google(audio)
        print(speech)

    except sr.UnknownValueError:
        print('could not understand')

    key = cv2.waitKey(1) & 0xFF

    if key == ord('w'):
        break
