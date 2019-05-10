import speech_recognition as sr
import cv2
import sys
import subprocess
from subprocess import call
import os
import pyttsx3
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font, Entry, Scrollbar
import threading

global window
global voiceOutput
global popup
global notesOutput
global commandOutput

time.sleep(5)

def notes():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=2)
    engine = pyttsx3.init()
    engine.setProperty('voice','com.apple.speech.synthesis.voice.daniel')
    i = 0
    speech = None

    commands = ['create new category', 'list notes', 'read all notes', 'read notes', 'add note', 'delete note']
    



    #variables
    adding_note = False
    continue_note = False
    note_text = None
    done = True
    read_notes = False
    conversation = 0
    save_array = []
    deleting = False
    delete_note = None

    while True:
        
        
        if conversation == 0:
            print('What would you like to do?')
            print('')
            commandOutput.insert(0, 'What would you like to do?')
            engine.say('What would you like to do?')
            engine.runAndWait()
            time.sleep(1)
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
    ##        r.energy_threshold = 0.5

        try:
            speech = r.recognize_google(audio)
            print(speech)
            voiceOutput.insert(0, speech)

            
                

        except sr.UnknownValueError:
            print('could not understand anything')
            engine.say('I could not understand you')
            engine.runAndWait()
            commandOutput.insert(0, 'could not understand')
            time.sleep(1)
            

        except KeyboardInterrupt:
            print('keyboard interrupt')
            break
                

        #if adding_note = true, save speech to add later
        if adding_note == True:
            
            note_text = speech
            
        if continue_note == True:
            
            note_text = speech

        if deleting == True:

            delete_note = speech
                
        if speech is not None:

            #list commands
            if 'list commands' in speech:
                engine.say('Listing commands')
                for command in commands:
                    engine.say(command)
                    engine.runAndWait()
            
            #create new category(new file)
            if 'create new category' in speech:
                f = open('notes/test.txt', 'w')
                engine.say('Creating a new category')
                engine.runAndWait()
                commandOutput.insert(0, 'Creating a new category')
                time.sleep(1)
                conversation = 0

            #read all notes
            if 'read all notes' in speech:
                notes = os.listdir('./notes')
                for note in notes:
                    #read note
                    note = note.split(".")
                    path = note[0] + '.' + note[1]
                    with open('notes/'+path, 'r') as notes:
                        for line in notes.readlines():
                            print(line, end='')
                            commandOutput.insert(0, line)
                            engine.say(line)
                            engine.runAndWait()
                            time.sleep(0.5) 
                    conversation = 0
                    
            #list notes
            if 'list notes' in speech:
                print('listing notes')
                commandOutput.insert(0, 'Listing notes')
                notes = os.listdir('./notes')
                for note in notes:
                    #read note
                    print(note)
                    commandOutput.insert(0, note)
                    engine.say(note)
                    engine.runAndWait()
                    time.sleep(0.5)
                conversation = 0
                
            #read specific notes           
            if 'read' in speech and 'all' not in speech:
                print('opening')
                commandOutput.insert(0, 'Opening notes')
                engine.say('Opening notes')
                engine.runAndWait()
                time.sleep(0.5) 
                #check if notes exist
                for note in os.listdir('./notes'):
                    note = note.split(".")
                    if note[0] in speech:
                        path = note[0] + '.' + note[1]
                        
                        with open('notes/'+path, 'r') as notes:
                            for line in notes.readlines():
                                print(line, end='')
                                commandOutput.insert(0, line)
                                engine.say(line)
                                engine.runAndWait()
                                time.sleep(0.5) 
                conversation = 0
                
            #add note
            if 'add note' in speech or adding_note == True:
                adding_note = True
                if conversation == 0:
                    #go ahead, start dictating note
                    print('Start Dictating Note')
                    commandOutput.insert(0, 'Start Dictating Note')
                    engine.say('Start dictating note')
                    engine.runAndWait()
                    time.sleep(0.5) 
                    conversation += 1
                
                if adding_note == True and note_text is not None:
                    with open('./notes/notes.txt', "a") as n:
                        
                        n.write('\n'+note_text)
                        n.close()
                        
                        if conversation == 1:
                            print('Added note: '+note_text)
                            engine.say('Added note'+note_text)
                            engine.runAndWait()
                            time.sleep(1) 
                            
                        adding_note = False
                        note_text = None
                        done = False
                        conversation += 1 

            if done == False:
                if conversation == 2:
                    #are you done with your note
                    print('are you done with your note?')
                    commandOutput.insert(0, 'are you done with your note?')
                    engine.say('Are you finished with this note?')
                    engine.runAndWait()
                    time.sleep(0.5) 
                    conversation += 1
                    adding_note = False
                if 'no' == speech or continue_note == True:
                    continue_note = True
                    if conversation == 3:
                        #continue to add your note
                        print('continue your note')
                        commandOutput.insert(0, 'continue your note')
                        engine.say('Please continue to dictate your note')
                        engine.runAndWait()
                        time.sleep(0.5)
                        conversation += 1
                        
                    if continue_note == True and note_text is not None:
                        with open('./notes/notes.txt', "a") as n:
                            n.write(' '+note_text)
                            
                            n.close()
                            print('Added note: '+note_text)
                            commandOutput.insert(0, 'added note: '+note_text)
                            engine.say('Added note '+note_text)
                            engine.runAndWait()
                            time.sleep(0.5)
                            continue_note = False
                            note_text = None
                            done = True
                            conversation = 0
                            
                if 'yes' in speech:
                    print('saving note')
                    commandOutput.insert(0,'saving note')
                    engine.say('Okay, saving note')
                    engine.runAndWait()
                    time.sleep(0.5) 
                    done = True
                    conversation = 0
                    continue_note = False
                    adding_note = False
                    
            #delete notes
            if 'delete' in speech or deleting == True:
                deleting = True
                if conversation == 0:
                    print('starting deleting process')
                    conversation += 1
                #reading notes, then you can delete
                    print('')
                    print('Current Notes')
                with open('notes/notes.txt', 'r') as notes:
                    lines = notes.readlines()
                    print(lines)
                    for line in lines:
                        print(line)
                            
                            
                if deleting == True and delete_note is not None:
                    #list lines youd like to delete
                    with open('notes/notes.txt', 'w') as n:
                        print('d',delete_note)
                        for line in lines:
                            line = line.split("\n")
                            print('l',line[0])
                            if line[0] == delete_note or line[0] in delete_note or line[0] in speech or delete_note in line[0]:
                                
                                print('will delete line: ', line)

                            else:
                                save_array.append(line[0])
                                
                        for note in save_array:
                            
                            n.write(note+'\n')
                            print('writing note:', note)
                        n.close()

                        deleting = False
                        delete_note = None
                    
                
                
                    
            if 'quit' in speech:
##                p = subprocess.Popen(['python', 'main.py'])
                quitFunction()
                break


        speech = '' 

        key = cv2.waitKey(1) & 0xFF

        if key == ord('w'):
            break

def quitFunction():
    print('quitting notes, starting main dashboard')
    window.destroy()
    p = subprocess.Popen(['python', 'main.py'])
    os._exit(13)
    
def addNotePopup():
    global popup
    global noteEntry
    
    popup = tk.Tk()
##    popup.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
    popup.geometry('480x320')
    popup.wm_title('add note')
    noteEntry = Entry(popup, width=18)
    noteEntry.place(x=175, y=100)
    addButton = tk.Button(popup, text = 'add',command= addNote, width=15)
    addButton.place(x=175, y=150)
    

def addNote() :
    print('added')
    noteInput = noteEntry.get()
    with open('./notes/notes.txt', "a") as n:
                        
        n.write('\n'+noteInput)
        n.close()
    
    popup.destroy()

def refresh():
    notesOutput.delete(0, 'end') 
   
    path = 'notes.txt'
    with open('notes/'+path, 'r') as notes:
        for line in notes.readlines():
            notesOutput.insert(0, line)
            print(line)
                    
def delete():
    save_array = []
    selection = notesOutput.curselection()
##    selected_text_list = [notesOutput.get(i) for i in notesOutput.curselection()]
    noteSelection = notesOutput.get(selection[0])
    print(noteSelection)

    with open('notes/notes.txt', 'r') as notes:
        lines = notes.readlines()
        
    
    with open('notes/notes.txt', 'w') as n:
            
        for line in lines:
            line = line.split("\n")
            print('l',line[0])
            if line[0] == noteSelection or line[0] in noteSelection or noteSelection in line[0]:
                
                                    
                print('will delete line: ', line)
                print(noteSelection)

            else:
                save_array.append(line[0])
                                
        for note in save_array:
                            
            n.write(note+'\n')
            print('writing note:', note)
            n.close()



t = threading.Thread(target=notes)
t.start()

window = tk.Tk()  
##window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
window.geometry('480x320')
buttonHeight = 4
buttonWidth = 15

font = font.Font(family='Helvetica', size=10, weight='bold')

n = ttk.Notebook(window)

f1 = ttk.Frame(n, width = 480, height = 320)
f2 = ttk.Frame(n, width = 480, height = 320)
f3 = ttk.Frame(n, width = 480, height = 320)


n.add(f1, text='Dashboard')
n.add(f2, text='Notes')
n.add(f3, text='Voice Log')
n.grid()

f1.grid_propagate(False)
f2.grid_propagate(False)
f3.grid_propagate(False)

addNoteButton= tk.Button(f1, text ="add note", command = addNotePopup, height = 5, width = buttonWidth)
addNoteButton.place(x=155,y=75)

scrollbar = Scrollbar(f2, orient="vertical")
scrollbar.pack(side="right", fill="y")
notesOutput = tk.Listbox(f2, yscrollcommand=scrollbar.set,height=10, width=25, font=font)
notesOutput.place(x=35, y=20)
scrollbar.config(command=notesOutput.yview)
notesOutput.config(yscrollcommand=scrollbar.set)


refreshButton= tk.Button(f2, text ="refresh", command = refresh , height = buttonHeight, width = buttonWidth)
refreshButton.place(x=300,y=20)

deleteButton= tk.Button(f2, text ="delete", command = delete , height = buttonHeight, width = buttonWidth)
deleteButton.place(x=300,y=100)

voiceOutput = tk.Listbox(f3, height=10, width=25, font=font)
voiceOutput.place(x=250, y=20)

commandOutput = tk.Listbox(f3, height=10, width=25, font=font)
commandOutput.place(x=35, y=20)

quitButton= tk.Button(f1, text ="quit", command = quitFunction, height = 3, width = 7)
quitButton.place(x=380,y=180)

  

window.mainloop()





