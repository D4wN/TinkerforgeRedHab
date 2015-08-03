from gui.gui_control import GuiControl
from util.event_logger import EventLogger
from profiling.profiler import Profiler

"""
/*---------------------------------------------------------------------------
                                AbstractRecognizer
 ---------------------------------------------------------------------------*/
"""
class AbstractRecognizer():
    def __init__(self):
        self._gui = GuiControl.Instance()

    def recognize(self, cb, args=None):
        raise Exception("AbstractRecognizer.recognize() not implemented!")

    def cb_recognize(self, recognized_name):
        raise Exception("AbstractRecognizer.cb_recognize() not implemented!")


"""
/*---------------------------------------------------------------------------
                                FaceRecognizer
 ---------------------------------------------------------------------------*/
"""
from thread import start_new_thread, allocate_lock
from recognition.faceDetectionWebcam import *
import recognition.generateFaceDatabase as gfd
import recognition.faceRecognition as fr
import recognition.utilities as util
from random import randint


class FaceRecognizer(AbstractRecognizer):
    def __init__(self, gui_component=None):
        self._gui = gui_component
        self._name = "[FaceRecognizer]"

        self._profiler = Profiler("[Profiler:Main]")

    def recognize(self, args=None):
        if args is None:
            EventLogger.warning(self._name + " did not get any args!")
            return None

        if len(args) != 2:
            EventLogger.error("Please start this Program with the parameter 1 or 0")
            return None

        if args[1] == "1":  # ------------------------------------------------| Create_Database_Mode
            EventLogger.info("Start Mode 1: Create Face Database")
            fdb = gfd.GenerateFaceDatabase("Roland")
            fdb.generate_face_database()

        elif args[1] == "2":  # ------------------------------------------------| Face_Recognition_Mode
            EventLogger.info("Start Mode 2: Face Recognition")
            fr_instance = fr.faceRecognition(self.cb_recognize)
            fr_instance.start_process()

        else:  # -----------------------------------------------------------------| Face_Detection_Mode
            EventLogger.info("Start Mode default: Detecting Faces")
            start_new_thread(face_detection_webcam, (self.__found_face,))


    def __found_face(self, frame, faces):
        '''
        This function is just for debugging purpose

        :param frame:
        :param faces:
        :return:
        '''
        if frame is None or faces is None:
            print "found_face: one param is None"

        max = len(faces)
        print "Found " + str(len(faces)) + " images"

        # process the faces
        for i, val in enumerate(faces):
            rnd = str(randint(0, 1000000))
            util.save_image("./image_" + str(i) + "_" + str(rnd) + ".pgm", val)

        #start_new_thread(self.__profile_process, (self.__callback_profile_process, "Marv", ))

    def cb_recognize(self, recognized_name):
        print "callbacked: " + str(recognized_name)
        p = Profiler("[Profiler-Main]")
        p.start_profile_routine(recognized_name, False)



class TestRecognizer(AbstractRecognizer):
    def __init__(self):
        AbstractRecognizer.__init__(self)

    def recognize(self, cb, args=None):
        from time import sleep

        print "DO SHIT! 5SEK LONG - args: " + str(args)
        sleep(5)
        print "DO SOomething else 2"
        sleep(2)
        print "DO SOomething finished"
        cb("MyName")

    def cb_recognize(self, recognized_name):
        print "callbacked: " + str(recognized_name)
        p = Profiler("[Profiler-Main]")
        p.start_profile_routine(recognized_name, False)
        #self._gui._db_recognizer_state_off()


