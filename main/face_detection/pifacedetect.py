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
time.sleep(2)

#start FPS counter
fps = FPS().start()

#loop over frames
while True:

    #resize frame to speed up processing
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    #convert input to gray for detection and rbg for recognition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #detect faces in grayscale frame
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    #reorder from (x,y,w,h) to (top,right,bottom,left)
    boxes = [(y,x+h,y+h,x) for (x,y,w,h) in rects]

    #compute facial embeddings
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    #loop over embeddings
    for encoding in encodings:

        #match face with input image
        matches = face_recognition.compare_faces(encodings, encoding)
        name = 'me'

        #check if we have a match
        if True in matches:

            #count number of times matches occured
            matchedIdxs = [i for (i,b) in enumerate(matches) if b]
            counts= {}

            #loop over matched indexes and count recognized faces
            for i in matchedIdxs:
                name = data['names'][i]
                counts[name] = counts.get(name, 0)+1

            #determine recognized face with most votes
            name = max(counts, key=counts.get)

        names.append(name)

        #loop over recognized faces
    for ((top, right, bottom, left), name) in zip(boxes, names):

        #draw face name on image
        cv2.rectangle(frame,(left,top), (right,bottom),
                      (0,255,0), 2)

        y = top -15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left,y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0),2)

    #display
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break


    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
    








    

