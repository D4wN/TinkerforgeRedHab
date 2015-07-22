import cv2
import sys
import numpy as np

faceCascade = cv2.CascadeClassifier('./res/haarcascade_frontalface_alt.xml')
video_capture = cv2.VideoCapture(0)

def face_detection_webcam(callback):
    '''
    Reads the frames from the std. video camera until it detects a face.
    :return:    frame, cleanImages
    '''

    while True:
        cleanImages = []
        frame = None
        faces = None

        ret, frame = video_capture.read()

        # numpy.ndarray is the type of the output
        # FIXME: should be checked (maxSize  and minSize)
        faces = faceCascade.detectMultiScale(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
            scaleFactor=1.1,
            minNeighbors=10,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        print "Found " + str(len(faces)) + " images" # FIXME: Debug msg

        # convert colored frame into gray frame
        gryFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # get only faces out of the frame
        for (x, y, w, h) in faces:
            cleanImages.append(cv2.cv.GetSubRect(cv2.cv.fromarray(gryFrame), (x, y, w, h)))

        if len(cleanImages) != 0:
            break

    # callback on detected face
    callback(frame, cleanImages)

def end_webcam():
    '''
    Will close the connection to the webcam
    :return:
    '''
    video_capture.release()
