#import packages
from imutils.video import VideoStream, FPS
import face_recognition
import imutils
import pickle
import time
import cv2


#initialize variables
cascade = 'haarcascade_frontalface_default.xml'
encodings = 'encodings.pickle'
data = pickle.loads(open(encodings, "rb").read())
detector = cv2.CascadeClassifier(cascade)

#start video stream
vs = VideoStream(src=0).start()
print('starting video stream')


#start FPS counter
fps = FPS().start()

tracker = cv2.TrackerMOSSE_create()
initBB = None

i = 0

num_frames = 0

#loop over frames
while True:

    #resize frame to speed up processing
    frame = vs.read()
    frame = imutils.resize(frame, width=400)

        

    
    #if not tracking yet
    
    if initBB is None or initBB == '':
        print('attempting to detect face')
        #convert input to gray for detection and rbg for recognition
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        #detect faces in grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
                    minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        print(rects, 'rects')
        
        #start tracker
        if len(rects) > 0:
        
            initBB = tuple(rects[0])
            print('starting tracker')
            tracker.init(frame, initBB)
            
    #if we are tracking       
    if initBB is not None:
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
            print(x, y, w, h)
            
            fps.update()
            fps.stop()
            
            if num_frames == 10:
                
                    
                if x in range(0, 125):
                    print('move left')
                if x in range(175,400):
                    print('move right')
                if x < 0:
                    print('out of frame, move left')
                if x > 400:
                    print('out of frame, move right')
                if y in range(0, 30):
                    print('move down')
                if y in range(230, 400):
                    print('move up')
                if y < 0:
                    print('out of frame, move down')
                if y > 400:
                    print('out of frame, move up')
                    
                num_frames = 0
                    
                
            num_frames += 1
            
##            print(fps.fps())
            

    #display
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break


    fps.update()
    i += 1
    num_frames += 1

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
    








    

