import cv2
import sys
import numpy as np
from util.event_logger import EventLogger
import utilities as util

faceCascade = cv2.CascadeClassifier('./recognition/res/haarcascade_frontalface_alt.xml')

WIDTH_DB_FACES = 92
HEIGHT_DB_FACES = 112

def face_detection_webcam(callback):
    '''
    Reads the frames from the std. video camera until it detects a face.
    :return:    frame, cleanImages
    '''

    video_capture = cv2.VideoCapture(0)

    # webcam setup
    video_capture.set(cv2.cv.CV_CAP_PROP_FPS, 5)
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

    if video_capture is None or not video_capture.isOpened():
        EventLogger.error("ERROR: Can't connect to Webcam")
        sys.exit(1)

    while True: #FIXME: Set timeout for detection
        cleanImages = []
        cleanSizedImages = []
        frame = None
        faces = None

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
            EventLogger.info("Found " + str(len(faces)) + " face/faces")

            # convert colored frame into gray frame
            gryFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # get only faces out of the frame
            for (x, y, w, h) in faces:
                original_face = cv2.cv.GetSubRect(cv2.cv.fromarray(gryFrame), (x, y, w, h))

                sized_face = cv2.cv.CreateImage((WIDTH_DB_FACES,HEIGHT_DB_FACES), 8, 1)
                cv2.cv.Resize(original_face, sized_face, interpolation=cv2.cv.CV_INTER_AREA)

                cleanImages.append(sized_face)

            if len(cleanImages) != 0:
                break

    video_capture.release()
    # callback on detected face
    callback(frame, cleanImages)