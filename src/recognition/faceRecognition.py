import cv2
import numpy as np
import random
import os

import utilities as util
from util.event_logger import EventLogger, ConsoleLogger
import faceDetectionWebcam as fdw

EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))

WIDTH_DB_FACES = 92
HEIGHT_DB_FACES = 112

class faceRecognition:
    def __init__(self, recognizied_callback):
        self.face_recognized_callback = recognizied_callback

        self.model_lbph = cv2.createLBPHFaceRecognizer()
        self.csvPath = ".%srecognition%sfaceDatabase%s" % (os.sep,os.sep,os.sep)

    def update_model(self):
        EventLogger.info("Face recognition training started")
        util.create_csv(self.csvPath)
        training_data = self.read_csv((self.csvPath + "faces.csv")).readlines()
        data_dict = self.create_label_matrix_dict(training_data)

        try:
            self.model_lbph.train(data_dict.values(), np.array(data_dict.keys()))
        except Exception as e:
            EventLogger.error("Error-Training: " + str(e))

        try:
            self.model_lbph.save(self.csvPath + "lbph-model.xml")
        except Exception as e:
            EventLogger.error(e)

        EventLogger.info("Face recognition training finished")

    def load_model(self):
        try:
            if os.path.isfile(self.csvPath + "lbph-model.xml"):
                self.model_lbph.load(self.csvPath + "lbph-model.xml")
                EventLogger.info("Loaded face rec-model: " + self.csvPath + "lbph-model.xml")
            else:
                raise Exception("No model was found. Will create a new one")

        except Exception as e:
            EventLogger.error(e)
            self.update_model()

    def read_csv(self, filename):
        EventLogger.info(filename)

        """ Read a csv file """
        csv = open(filename, 'r')
        return csv

    def create_label_matrix_dict(self, input_file):
        """ Create dict of label -> matricies from file """
        label_dict = {}

        for line in input_file:
            filename, label = line.strip().split(';')

            ##update the current key if it exists, else append to it
            if label_dict.has_key(int(label)):
                current_files = label_dict.get(label)
                np.append(current_files, self.read_matrix_from_file(filename))
            else:
                label_dict[int(label)] = self.read_matrix_from_file(filename)

        return label_dict

    def read_matrix_from_file(self, filename):
        """ read in grayscale version of image from file """
        return cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)

    def _recognize_face(self,frame, faces):
        if len(faces) == 0:
            self.face_recognized_callback("No-Face-Detected")
            return

        self.load_model()
        for img in faces:
            rnd = random.randint(0, 10000000)
            path_file = "./recognition/tmp/" + str(rnd) + ".pgm"
            util.save_image(path_file, img)

            # fix the size of the input image If needed
            sized_face = None
            input_image = self.read_matrix_from_file(path_file)
            width, height = cv2.cv.GetSize(cv2.cv.fromarray(input_image))

            if height != HEIGHT_DB_FACES or width != WIDTH_DB_FACES:
                sized_face = cv2.cv.CreateImage((WIDTH_DB_FACES, HEIGHT_DB_FACES), 8, 1)
                cv2.cv.Resize(input_image, sized_face, interpolation=cv2.cv.CV_INTER_CUBIC)
            else:
                sized_face = input_image

            # actual face recognition
            EventLogger.info("Started prediction")
            predicted_label_lbph, conf_lbph = self.model_lbph.predict(sized_face)
            EventLogger.info('LBPH: Predicted: %(predicted)s Confidence : %(confidence )s ' % {"predicted": predicted_label_lbph, "confidence ":conf_lbph})

            try:
                os.remove(path_file)
            except Exception as e:
                EventLogger.error(e)

            if conf_lbph <= 110:
                user = util.get_real_user( self.csvPath, predicted_label_lbph)
                self.face_recognized_callback(user)
            else:
                self.face_recognized_callback("Non-Index")

    def start_process(self):
        fdw.face_detection_webcam(self._recognize_face)