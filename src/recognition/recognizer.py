from gui.gui_control import GuiControl
from lib.brick_red import RED
from profiling.profileDecider import FaceCounterData, ProfileDecider
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
from thread import start_new_thread
from recognition.faceDetectionWebcam import *
import recognition.generateFaceDatabase as gfd
import recognition.faceRecognition as fr
import recognition.utilities as util
from random import randint

class FaceRecognizer(AbstractRecognizer):
    def __init__(self):
        AbstractRecognizer.__init__(self)

        self._name = "[FaceRecognizer]"
        self._profiler = Profiler("[Profiler:Main]")

    def recognize(self, cb, args=None):
        recognized_name = None

        if args is None:
            EventLogger.warning(self._name + " did not get any args!")
            cb("NO NAME")

        if len(args) != 2:
            EventLogger.error("Please start this Program with the parameter 1 or 0")
            cb("NO NAME")

        if args[1] == 1:  # ------------------------------------------------| Create_Database_Mode
            EventLogger.info("Start Mode 1: Create Face Database")
            fdb = gfd.GenerateFaceDatabase("Roland")
            fdb.generate_face_database()
            cb("NO NAME")

        elif args[1] == 2:  # ------------------------------------------------| Face_Recognition_Mode
            EventLogger.info("Start Mode 2: Face Recognition")
            fr_instance = fr.faceRecognition(cb)
            fr_instance.start_process()

        else:  # -----------------------------------------------------------------| Face_Detection_Mode
            EventLogger.info("Start Mode default: Detecting Faces")
            start_new_thread(face_detection_webcam, (self.__found_face,))
            cb("NO NAME")

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

            # start_new_thread(self.__profile_process, (self.__callback_profile_process, "Marv", ))

    def cb_recognize(self, recognized_name):
        print "callbacked: " + str(recognized_name)
        self._profiler.start_profile_routine(recognized_name, False)

"""
/*---------------------------------------------------------------------------
                                NfcRfidRecognizer
 ---------------------------------------------------------------------------*/
"""

class NfcRfidRecognizer(AbstractRecognizer):
    def __init__(self):
        AbstractRecognizer.__init__(self)

        self._name = "[NfcRfidRecognizer]"
        self._profiler = Profiler("[Profiler-NfcRfidRecognizer]")
        # self._gui._nfc_init()

        self._counter = 0
        self._exit_timer = None
        self._exit_cb = None

    def recognize(self, cb, args=None):
        if args != None:
            self.__write_mode(args[0])

        EventLogger.info("NFC/RFID Recognizer started...")
        self._counter = 0

        if self._gui._nfc is None:
            EventLogger.warning(self._name + " NFC/RFID Component was initialized!")

        # Rufe request_tag_id() auf

        self._gui._nfc_cb_to_profiler = cb
        self._exit_cb = cb

        self._gui._nfc.request_tag_id(self._gui._nfc.TAG_TYPE_TYPE2)
        self._exit_timer = threading.Timer(2, self.__cb_retry)
        self._exit_timer.start()

    def cb_recognize(self, recognized_name):
        self._exit_timer.cancel()
        self._gui._nfc_write_name = None
        self._gui._nfc_write_mode = False

        EventLogger.debug(self._name + " cd_recognized= " + str(recognized_name))
        EventLogger.info("NFC/RFID Recognizer finished...")

        if recognized_name != "NO NAME":
            self._profiler.start_profile_routine(recognized_name)

    def __cb_retry(self):
        EventLogger.info("Try to read the Tag...")
        # print "Counter: " + str(self._counter)

        if self._counter >= 5:
            EventLogger.info("Tried 5 times to read the Tag!")
            self._exit_cb("NO NAME")
            return

        self._counter += 1
        self._gui._nfc.request_tag_id(self._gui._nfc.TAG_TYPE_TYPE2)
        # TODO thread.restart?
        self._exit_timer = threading.Timer(2, self.__cb_retry)
        self._exit_timer.start()

    def __write_mode(self, name):
        EventLogger.info("NFC/RFID write Mode: Writing " + str(name) + " to the Tag.")
        self._gui._nfc_write_name = name
        self._gui._nfc_write_mode = True

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
        p.start_profile_routine(recognized_name, True)
        # self._gui._db_recognizer_state_off()

class FaceCountRecognizer(AbstractRecognizer):
    def __init__(self):
        AbstractRecognizer.__init__(self)

        self._name = "[FaceCountRecognizer]"
        self._profiler = Profiler("[Profiler-FaceCountRecognizer]")

        # Tinkervision
        self._ipcon = None

        # Vision Callback specific
        self._exit_cb = None

        self.decider = ProfileDecider()

    def release(self):
        EventLogger.debug(self._name + " released.")

        if self._ipcon is None:
            return

        # TODO close rest
        result = self._red.vision_remove_all_modules()  # TODO implemnt remove_module with ide -> still bugged!
        EventLogger.info(self._name + "Removed Vision Module.(" + str(result) + ")")
        EventLogger.info(self._name + "Running ModuleCount: " + str(self._red.vision_libs_loaded_count()))

    def recognize(self, cb, args=None):
        # if self._ipcon is None: # init is now in recognition_runner.__init__
        #    self._init_red()
        # EventLogger.debug(self._name + " Module(" + str(self._vision_module.id) + ") restart = " +
        #                   str(self._red.vision_module_restart(self._vision_module.id)))

        self._exit_cb = cb
        # self._cb_counter = 0

        EventLogger.info(self._name + " started.")

        #FIXME DEBUG ONLYY
        ProfileDecider.CALLBACK_BUFFER.append(FaceCounterData(self._vision_module.id, 26, 0, 0, 0, "Nope"))
        ProfileDecider.CALLBACK_BUFFER.append(FaceCounterData(self._vision_module.id, 20, 0, 0, 0, "Nope"))
        ProfileDecider.CALLBACK_BUFFER.append(FaceCounterData(self._vision_module.id, 6, 0, 0, 0, "Nope"))
        ProfileDecider.CALLBACK_BUFFER.append(FaceCounterData(self._vision_module.id, 26, 0, 0, 0, "Nope"))
        ProfileDecider.CALLBACK_BUFFER.append(FaceCounterData(self._vision_module.id, 16, 0, 0, 0, "Nope"))


        # check if enough values were given by callbacks
        if len(ProfileDecider.CALLBACK_BUFFER.get()) < ProfileDecider.CALLBACK_BUFFER_SIZE:
            EventLogger.info(
                self._name + " Recognition process could not be started. Please wait a bit, until enought Data is present. (Data " + str(
                    len(ProfileDecider.CALLBACK_BUFFER.get())) + "x collected, " + str(
                    ProfileDecider.CALLBACK_BUFFER_SIZE) + " needed!)")
            return

        self.decider.decide(self._exit_cb)


    def cb_recognize(self, recognized_name):
        # EventLogger.debug(self._name + " Module(" + str(self._vision_module.id) + ") stopped = " + str(
        #     self._red.vision_module_stop(self._vision_module.id)))

        EventLogger.debug(self._name + " recognized_name = " + str(recognized_name))
        EventLogger.info(self._name + " finished... TODO start profiler!")

        # TODO start profiler
        if recognized_name is None:
            EventLogger.info(self._name + " No Profile given. Nothing changed.")
            return

        if recognized_name != "NO NAME":
            ProfileDecider.CURRENT_ACTIVE_PROFILE = recognized_name
            self._profiler.start_profile_routine(recognized_name, True)

    def _init_red(self):
        self._ipcon = self._gui._ipcon
        # RED
        self._RED_UID = "3dfBkF"
        self._red = RED(self._RED_UID, self._ipcon)
        self._red.register_callback(RED.CALLBACK_VISION_MODULE, self.__vision_callback)

        self._vision_module = self._red.vision_module_start("cascadeclassifier")  #
        if self._vision_module.result != 0:
            msg = self._name + " VisionModule could not be started! Please see the Error Logs on the REDBrick. Err(" + str(
                self._vision_module.result) + ")"
            EventLogger.error(msg)
            raise Exception(msg)
            # EventLogger.debug(self._name + " INIT-Module(" + str(self._vision_module.id) + ") stopped = " + str(
            #     self._red.vision_module_stop(self._vision_module.id)))

            # sleep(1)

    def __vision_callback(self, id, x, y, w, h, msg):
        return

        if self._vision_module.id != id:
            EventLogger.debug(self._name + " Vision Callback wrong ID(" + str(id) + ")")
            return

        if x == -1:
            EventLogger.debug(self._name + " x == -1 No Valid Callback")
            # return # FIXME implement when callbakcs fixed!

        # FIXME <---------------------------------------------------------------------------------------------------------######################################
        # only debugging values!
        import random
        x = random.randint(3, 10)

        # self._cb_counter += 1  # only register valid callbacks
        ProfileDecider.CALLBACK_BUFFER.append(FaceCounterData(id, x, y, w, h, msg))
        print data
