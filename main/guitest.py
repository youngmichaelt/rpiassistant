import tkinter as tk


window = tk.Tk()  
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

trackerButton = tk.Button(window, text ="Start Notes", command = window.destroy, height = 5, width = 20)
trackerButton.place(x=0, y=0)

notesButton = tk.Button(window, text ="Start Tracker", command = window.destroy, height = 5, width = 20)
notesButton.place(x=250, y=0)

quitButton= tk.Button(window, text ="quit", command = window.destroy, height = 5, width = 20)
quitButton.place(x=1000,y=0)

window.mainloop()  
