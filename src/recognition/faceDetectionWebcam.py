import cv2
import sys
import numpy as np
from util.event_logger import EventLogger

faceCascade = cv2.CascadeClassifier('./res/haarcascade_frontalface_alt.xml')
video_capture = cv2.VideoCapture(0)

def face_detection_webcam(callback):
    '''
    Reads the frames from the std. video camera until it detects a face.
    :return:    frame, cleanImages
    '''

    if video_capture is None or not video_capture.isOpened():
        EventLogger.error("ERROR: Can't connect to Webcam")
        sys.exit(1)

    while True:
        cleanImages = []
        frame = None
        faces = None

        _, frame = video_capture.read()

        # numpy.ndarray is the type of the output
        # FIXME: should be checked (maxSize  and minSize)
        faces = faceCascade.detectMultiScale(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
            scaleFactor=1.1,
            minNeighbors=10,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        EventLogger.info("Found " + str(len(faces)) + " face/faces")

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
    EventLogger.info("Close connection to the webcam")
    video_capture.release()
