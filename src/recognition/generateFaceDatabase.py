import cv2
import os

import utilities as util
import faceDetectionWebcam as fdw

faceCascade = cv2.CascadeClassifier('./res/haarcascade_frontalface_alt.xml')
video_capture = cv2.VideoCapture(0)
MAX_IMAGES = 10

class GenerateFaceDatabase:
    def __init__(self, name):
        self.userPath = util.create_dir(name)
        self.index = 0

    def _found_face(self, frame, faces):
         for img in faces:
            util.save_image(self.userPath + "/" + str(self.index) + ".pgm", img)
            self.index += 1

    def generate_face_database(self):
        # start capturing
        # TODO: check on first image if there is already an entry for this user ?
        for i in range(0, MAX_IMAGES):
            fdw.face_detection_webcam(self._found_face)

        video_capture.release()