import cv2
import sys
import numpy as np
from util.event_logger import EventLogger
import utilities as util
import threading

faceCascade = cv2.CascadeClassifier('./recognition/res/haarcascade_frontalface_alt.xml')
video_capture = None

WIDTH_DB_FACES = 92
HEIGHT_DB_FACES = 112

TIMER_EXIT = False

def _stop_webcam():
    global TIMER_EXIT
    TIMER_EXIT = True
    EventLogger.info("Webcam timeout reached")

def face_detection_webcam(callback):
    '''
    Reads the frames from the std. video camera until it detects a face.
    :return:    frame, cleanImages
    '''
    global TIMER_EXIT
    global video_capture

    if video_capture is None or not video_capture.isOpened():   # initial start
        video_capture = cv2.VideoCapture(0)

    # webcam setup
    video_capture.set(cv2.cv.CV_CAP_PROP_FPS, 5)
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

    if not video_capture.isOpened():
        EventLogger.error("ERROR: Can't connect to Webcam")
        sys.exit(1)

    exit_timer = threading.Timer(60, _stop_webcam)
    exit_timer.start()

    cleanImages = []
    frame = None
    faces = None

    while not TIMER_EXIT:
        if not video_capture.grab():
            continue

        _, frame = video_capture.retrieve()
        # _, frame = video_capture.read()
        if frame is not None:
            # numpy.ndarray is the type of the output
            # FIXME: should be checked (maxSize  and minSize)
            faces = faceCascade.detectMultiScale(
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                scaleFactor=1.1,
                minNeighbors=10,
                minSize=(30, 30),
                flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            # convert colored frame into gray frame
            gryFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # get only faces out of the frame
            for (x, y, w, h) in faces:
                original_face = cv2.cv.GetSubRect(cv2.cv.fromarray(gryFrame), (x, y, w, h))

                sized_face = cv2.cv.CreateImage((WIDTH_DB_FACES,HEIGHT_DB_FACES), 8, 1)
                cv2.cv.Resize(original_face, sized_face, interpolation=cv2.cv.CV_INTER_CUBIC)

                cleanImages.append(sized_face)

            if len(cleanImages) != 0:
                EventLogger.info("Face/es detected " + str(len(cleanImages)) )
                exit_timer.cancel()
                break

    video_capture.release()
    EventLogger.info("Closed connection to the webcam")

    TIMER_EXIT = False
    # callback on detected face
    callback(frame, cleanImages)