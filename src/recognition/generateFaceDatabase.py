import cv2
import os

import utilities as util
import faceDetectionWebcam as fdw
from util.event_logger import EventLogger
import recognition.faceRecognition as fre

MAX_IMAGES = 10

class GenerateFaceDatabase:
    def __init__(self, name):
        self.userPath = util.create_dir(name)
        self.index = 1

    def _duplicated_index_check(self, results):
            print str(results)

    def _found_face(self, frame, faces):
         for img in faces:
            imgPath = self.userPath + "/" + str(self.index) + ".pgm"
            EventLogger.info("Save Image: " + imgPath)
            util.save_image(imgPath, img)
            self.index += 1

    def generate_face_database(self):
        # start capturing
        try:
            fr_instance = fre.faceRecognition(self._duplicated_index_check)
            fr_instance.start_process()
        except Exception as e:
             EventLogger.error(e)

        try:
            for i in range(0, MAX_IMAGES):
                fdw.face_detection_webcam(self._found_face)

            # update model
            fr = fre.faceRecognition(self._duplicated_index_check)
            fr.update_model()

        except Exception as e:
            EventLogger.error(e)