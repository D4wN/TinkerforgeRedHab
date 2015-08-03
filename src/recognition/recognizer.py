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
import recognition.faceRecognitionEigenfaces as fre
import recognition.utilities as util
from random import randint


class FaceRecognizer(AbstractRecognizer):
    def __init__(self, gui_component=None):
        self._gui = gui_component
        self._name = "[FaceRecognizer]"

        self._process = False
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
            fr_instance = fre.faceRecognitionEigenfaces()
            fr_instance.start_process()

        else:  # -----------------------------------------------------------------| Face_Detection_Mode
            EventLogger.info("Start Mode default: Detecting Faces")
            try:
                lock = allocate_lock()
                self._process = False
                #print "face_state = " + str(face_recognition_state) + "\nface_running: " + str( face_recognition_running) + "\nprocess: " + str(process) + "\n---"
                while face_recognition_running:
                    if not self._process:  #and face_recognition_state:
                        lock.acquire()
                        self._process = True
                        lock.release()

                        print "STARTED"
                        start_new_thread(face_detection_webcam, (self.__found_face,))

                raise KeyboardInterrupt

            except KeyboardInterrupt:
                EventLogger.info("Will now end this program")

    def __found_face(self, frame, faces):

        if frame is None or faces is None:
            print "found_face: one param is None"

        max = len(faces)
        print "Found " + str(len(faces)) + " images"

        # process the faces
        for i, val in enumerate(faces):
            rnd = str(randint(0, 1000000))
            # 'cv2.cv.cvmat'
            util.save_image("./image_" + str(i) + "_" + str(rnd) + ".pgm", val)
            # util.save_image("./frame_" + str(rnd) + ".jpeg", (cv2.cv.fromarray(frame)))
            #util.show_image("Face", val )


        # FIXME: same face as last frame
        # Eigenfaces/Fishfaces

        # global process
        print "finished"
        # TODO GUI
        #db.set_selected_led_state(DualButton.LED_LEFT, DualButton.LED_STATE_OFF)

        face_recognition_state = False
        self._process = False

        start_new_thread(self.__profile_process, (self.__callback_profile_process, "Marv", ))

    def __look_for_face(self):
        face_detection_webcam(self.__found_face)

    def __profile_process(self, cb, profile_name):
        EventLogger.debug("profile_process started--------------")
        msg = "Working... as intended!"

        if not profile_name or profile_name == "":
            msg = "No Profile Name was given!"
            EventLogger.error(msg)
            cb(msg)

        else:
            # TODO remove mode, when?
            msg = self._profiler.start_profile_routine(profile_name)
            cb(msg)

    def __callback_profile_process(self, msg):
        # TODO give the user the messages?
        EventLogger.debug("callback_profile_process started-----")
        EventLogger.debug("callback_profile_process MSG: " + str(msg))
        EventLogger.debug("callback_profile_process finished----")


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


