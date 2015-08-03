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
        # select mode for the face recognition

        self.model_eigenfaces = cv2.createEigenFaceRecognizer()
        #self.model_fisherfaces = cv2.createFisherFaceRecognizer()
        #self.model_lbph = cv2.createLBPHFaceRecognizer()

        sep = os.sep
        self.csvPath = ".%srecognition%sfaceDatabase%s" % (sep,sep,sep)


    def create_and_train_model_from_dict(self, label_matrix):
        """ Create eigenface model from dict of labels and images """
        #FIXME: If there is a model and nothing changed -> load the model
        # Else:
        self.model_eigenfaces.train(label_matrix.values(), np.array(label_matrix.keys()))
        #self.model_fisherfaces.train(label_matrix.values(), np.array(label_matrix.keys()))
        #self.model_lbph.train(label_matrix.values(), np.array(label_matrix.keys()))

        '''
        try:
           self.model.save("./recognition/faceDatabase/eigenface-model.xml")
        except Exception as e:
            EventLogger.error(e)
        '''

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
        training_data = self.read_csv(("./recognition/faceDatabase/faces.csv")).readlines()
        data_dict = self.create_label_matrix_dict(training_data)
        if len(data_dict) == 0:
            EventLogger.error("There is no face database available")
            return

        self.create_and_train_model_from_dict(data_dict)
        cv2.namedWindow("webcam_face")

        for img in faces:
            rnd = random.randint(0, 10000000)
            path_file = "./recognition/tmp/" + str(rnd) + ".pgm"
            util.save_image(path_file, img)

            sized_face = None
            input_image = self.read_matrix_from_file(path_file)

            height, width, channels = input_image.shape
            if height != HEIGHT_DB_FACES or width != WIDTH_DB_FACES:
                sized_face = cv2.cv.CreateImage((WIDTH_DB_FACES,HEIGHT_DB_FACES), 8, 1)
                cv2.cv.Resize(input_image, sized_face, interpolation=cv2.cv.CV_INTER_CUBIC)
            else:
                sized_face = input_image

            predicted_label_eigenfaces, conf_eigenfaces = self.model_eigenfaces.predict(sized_face)
            cv2.imshow("webcam_face", self.read_matrix_from_file(path_file))

            #predicted_label_fisherfaces, conf_fisherfaces = self.model_fisherfaces.predict(self.read_matrix_from_file(path_file))
            #predicted_label_lbph, conf_lbph = self.model_lbph.predict(self.read_matrix_from_file(path_file))

            EventLogger.info('Eigenfaces: Predicted: %(predicted)s Confidence : %(confidence )s ' % {"predicted": predicted_label_eigenfaces, "confidence ":conf_eigenfaces})
            #EventLogger.info('Fisherfaces: Predicted: %(predicted)s Confidence : %(confidence )s ' % {"predicted": predicted_label_fisherfaces, "confidence ":conf_fisherfaces})
            #EventLogger.info('LBPH: Predicted: %(predicted)s Confidence : %(confidence )s ' % {"predicted": predicted_label_lbph, "confidence ":conf_lbph})

            try:
                os.remove(path_file)
            except Exception as e:
                EventLogger.error(e)

            index = util.get_id_of_index( self.csvPath, predicted_label_eigenfaces)
            self.face_recognized_callback(index)

    def start_process(self):
        util.create_csv( self.csvPath)
        fdw.face_detection_webcam(self._recognize_face)