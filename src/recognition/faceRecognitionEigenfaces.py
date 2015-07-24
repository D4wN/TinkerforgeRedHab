import cv2
import numpy as np
import random
import os

import utilities as util
from util.event_logger import EventLogger, ConsoleLogger
import faceDetectionWebcam as fdw

EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))

class faceRecognitionEigenfaces:
    def __init__(self):
        pass

    def create_and_train_model_from_dict(self, label_matrix):
        """ Create eigenface model from dict of labels and images """
        model = cv2.createEigenFaceRecognizer()
        model.train(label_matrix.values(), np.array(label_matrix.keys()))
        return model

    def read_csv(self, filename):
        EventLogger.info(filename)

        """ Read a csv file """
        csv = open(filename, 'r')
        return csv

    def create_label_matrix_dict(self, input_file):
        """ Create dict of label -> matricies from file """
        ### for every line, if key exists, insert into dict, else append
        label_dict = {}

        for line in input_file:
            ## split on the ';' in the csv separating filename;label
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

    def _found_face(self,frame, faces):
        training_data = self.read_csv(("./recognition/faceDatabase/faces.csv")).readlines()
        data_dict = self.create_label_matrix_dict(training_data)
        model = self.create_and_train_model_from_dict(data_dict)

        for img in faces:
            rnd = random.randint(0, 10000000)
            path_file = "./recognition/tmp/" + str(rnd) + ".pgm"
            util.save_image(path_file,img)

            predicted_label = model.predict(self.read_matrix_from_file(path_file))
            for i in predicted_label:
                #TODO: return index to Marvs module
                print 'Predicted: %(predicted)s ' % {"predicted": i}
            try:
                os.remove(path_file)
            except Exception as e:
                EventLogger.error(e)

    def start_process(self):
        csvPath = "./recognition/faceDatabase"
        util.create_csv(csvPath)
        fdw.face_detection_webcam(self._found_face)