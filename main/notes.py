import speech_recognition as sr
import cv2
import sys
import subprocess
from subprocess import call
import os

r = sr.Recognizer()
mic = sr.Microphone(device_index=2)
i = 0
speech = None



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
    
    
    print('speak')
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
##        r.energy_threshold = 0.5

    try:
        speech = r.recognize_google(audio)
        print(speech)

        
            

    except sr.UnknownValueError:
        print('could not understand')   

    #if adding_note = true, save speech to add later
    if adding_note == True:
        
        note_text = speech
        
    if continue_note == True:
        
        note_text = speech

    if deleting == True:

        delete_note = speech
            
    if speech is not None:

        
        
        #create new category(new file)
        if 'create new category' in speech:
            f = open('notes/test.txt', 'w')

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
            
            

            
        #list notes
        if 'list notes' in speech:
            print('listing notes')
            notes = os.listdir('./notes')
            for note in notes:
                #read note
                print(note)
                    
        #read specific notes           
        if 'read' in speech and 'all' not in speech:
            print('opening')
            #check if notes exist
            for note in os.listdir('./notes'):
                note = note.split(".")
                if note[0] in speech:
                    path = note[0] + '.' + note[1]
                    
                    with open('notes/'+path, 'r') as notes:
                        for line in notes.readlines():
                            print(line, end='')

        #add note
        if 'add note' in speech or adding_note == True:
            adding_note = True
            if conversation == 0:
                #go ahead, start dictating note
                conversation += 1
            
            if adding_note == True and note_text is not None:
                with open('./notes/notes.txt', "a") as n:
                    
                    n.write('\n'+note_text)
                    n.close()
                    
                    if conversation == 1:
                        print('Added note: '+note_text)
                        
                    adding_note = False
                    note_text = None
                    done = False
                    conversation = 0 

        if done == False:
            if conversation == 0:
                #are you done with your note
                print('are you done with your note?')
                conversation += 1
            if 'no' in speech or continue_note == True:
                continue_note = True
                if conversation == 1:
                    #continue to add your note
                    print('continue your note')
                    
                if continue_note == True and note_text is not None:
                    with open('./notes/notes.txt', "a") as n:
                        n.write(' '+note_text)
                        
                        n.close()
                        print('Added note: '+note_text)
                        continue_note = False
                        note_text = None
                        done = True
                        conversation = 0
                        
            if 'yes' in speech:
                print('saving note')
                done = True
                conversation = 0

        if 'delete notes' in speech or deleting == True:
            deleting = True
            print('starting deleting process')
            #reading notes, then you can delete
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
                
            
            
                
        if 'stop notes' in speech:
            p = subprocess.Popen(['python', 'main.py'])
            break

            
            
            
                
                
                
            


                    
                    
##        if 'no' in speech and read_notes == True:
##            read_notes = False
                
            
        



    speech = '' 

    key = cv2.waitKey(1) & 0xFF

    if key == ord('w'):
        break
    



##with open('notes.txt', 'w') as notes:
##    notes.write('milk')

##with open('notes/notes.txt', 'r') as notes:
##    for line in notes.readlines():
##        print(line, end='')
