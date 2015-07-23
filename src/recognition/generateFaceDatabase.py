import cv2
import os

import utilities as util
import faceDetectionWebcam as fdw
from util.event_logger import EventLogger

MAX_IMAGES = 10

class GenerateFaceDatabase:
    def __init__(self, name):
        self.userPath = util.create_dir(name)
        self.index = 1

    def _found_face(self, frame, faces):
         for img in faces:
            imgPath = self.userPath + "/" + str(self.index) + ".pgm"
            EventLogger.info("Save Image: " + imgPath)
            util.save_image(imgPath, img)
            self.index += 1

    def generate_face_database(self):
        # start capturing
        # TODO: check on first image if there is already an entry for this user ?
        try:
            for i in range(0, MAX_IMAGES):
                fdw.face_detection_webcam(self._found_face)

            # create csv
            csvPath = "./recognition/faceDatabase"
            util.create_csv(csvPath)

        except Exception as e:
            EventLogger.error(e)
        finally:
            fdw.end_webcam()