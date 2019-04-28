##from threading import Thread
##import track
##
##def one(): import track
##def two(): import voicecommand
##
##Thread(target=two).start()
##Thread(target=one).start()
import os
os.system('python trackwmotion.py &')
os.system('python voice_command.py &')

##import track
##import voice_command
##
##track.function()
##voice_command.function()
