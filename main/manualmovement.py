
import tkinter as tk
from tkinter import font, ttk
import pigpio
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
p = GPIO.PWM(7, 50)
##p.start(7.5)
p.start(0)

##
def forward():
    print('firward')
    p.ChangeDutyCycle(7.5)
    time.sleep(2)
    p.ChangeDutyCycle(0)
    
##
def backward():
    print('BACK')
##    pi.set_servo_pulsewidth(3, 0)
##    pi.stop()
##
##def left():
##    break
##
##def right():
##    break
##
##def quitFunction():
##    break

window = tk.Tk()  
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))




font = font.Font(family='Helvetica', size=20, weight='bold')




height = 4
width = 10

forwardButton = tk.Button(window, text ="Forward", command = forward, height = height, width = width)
forwardButton.place(x=190, y=10)
##forwardButton.grid(column=3, row=10)
##forwardButton.pack(side='top', expand='yes')

backwardButton = tk.Button(window, text ="Backward", command = backward, height = height, width = width)
backwardButton.place(x=190, y=190)
##backwardButton.pack(side='top')


leftButton= tk.Button(window, text ="Left", command = window.destroy, height = height, width = width)
leftButton.place(x=99,y=100)

rightButton= tk.Button(window, text ="Right", command = window.destroy, height = height, width = width)
rightButton.place(x=281,y=100)

quitButton= tk.Button(window, text ="Quit", command = window.destroy, height = 3, width = 8)
quitButton.place(x=375,y=200)


window.mainloop()
