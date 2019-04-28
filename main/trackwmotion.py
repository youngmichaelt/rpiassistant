#import packages
from imutils.video import VideoStream, FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
p = GPIO.PWM(3, 50)
##p.start(7.5)
p.start(0)





#initialize variables
cascade = 'haarcascade_frontalface_default.xml'
##encodings = 'encodings.pickle'
##data = pickle.loads(open(encodings, "rb").read())
detector = cv2.CascadeClassifier(cascade)

#start video stream
vs = VideoStream(src=0).start()
print('starting video stream')


#start FPS counter
fps = FPS().start()

tracker = cv2.TrackerKCF_create()
initBB = None

success_list = []

i = 0

num_frames = 0
tracking = False

#loop over frames
while True:

    #resize frame to speed up processing
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

        

    
    #if not tracking yet
    
##    if initBB is None or initBB == '':
    if tracking == False:
        print('attempting to detect face')
        #convert input to gray for detection and rbg for recognition
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        #detect faces in grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                    minNeighbors=10, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        print(rects)
        
        #start tracker
        if len(rects) > 0:
        
            initBB = tuple(rects[0])
            print('starting tracker')
            tracker.clear()
            tracker = cv2.TrackerMOSSE_create()

            tracker.init(frame, initBB)
            tracking = True
            
    #if we are tracking       
##    if initBB is not None:
    if tracking == True:
        (success, box) = tracker.update(frame)
        
        if len(success_list) > 10:
            success_list = []
            tracking = False
            
        if success:

            success_list = []
            
            
            (x, y, w, h) = [int(v) for v in box]
            x2 = x-50
            y2 = y-50
            w2 = w*2
            h2 = h*2
            cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2),
				(0, 255, 0), 2)
            print(x2, y2, w2, h2)
            
            
            
            if num_frames % 2 == 0:
                
                    
                if x in range(0, 125):
                    print('move left')

                    

                    
                if x in range(175,400):
                    print('move right')
                if x < 50:
                    print('out of frame, move left')
                    
                            
                    try:
                        p.ChangeDutyCycle(7.5)
                        time.sleep(.025)
                        p.ChangeDutyCycle(0)
                        
                    except KeyboardInterrupt:
                        p.stop()
                        GPIO.cleanup()
                if x > 250:
                    print('out of frame, move right')
                    try:
                        p.ChangeDutyCycle(1.5)
                        time.sleep(.025)
                        p.ChangeDutyCycle(0)
                        
                    except KeyboardInterrupt:
                        p.stop()
                        GPIO.cleanup()
                if y in range(0, 30):
                    print('move down')
                if y in range(230, 400):
                    print('move up')
                if y < 0:
                    print('out of frame, move down')
                if y > 400:
                    print('out of frame, move up')
            fps.update()
            fps.stop()
        if not success:
            success_list.append(1)
##            tracker.clear()
            
##            tracking = False
                
                    
                
##            num_frames += 1
            
##            print(fps.fps())
            

    #display
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        p.stop()
        break


    fps.update()
    i += 1
    num_frames += 1

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
    








    

