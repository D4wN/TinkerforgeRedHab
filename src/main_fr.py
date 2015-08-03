from thread import start_new_thread, allocate_lock
from random import randint
import sys

# own imports
from gui.gui_control import GuiControl
from profiling.profiler import Profiler
from recognition.faceDetectionWebcam import *
import recognition.generateFaceDatabase as gfd
import recognition.faceRecognitionEigenfaces as fre
from recognition.recognizer import FaceRecognizer, TestRecognizer
import recognition.utilities as util
from util.event_logger import EventLogger, ConsoleLogger
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_dual_button import DualButton

# HOST = "localhost"
# PORT = 4223
# DB_UID = "mAo"
# db = None

# profiler = Profiler("[Profiler:Main]")

# control values
face_recognition_state = False
face_recognition_running = True
button_right_state = False
process = False


# def __cb_state_changed(button_l, button_r, led_r, led_l):
# global face_recognition_state, face_recognition_running, process
#
#     if button_r == DualButton.BUTTON_STATE_PRESSED:
#         led_r = DualButton.LED_STATE_OFF
#         db.set_selected_led_state(DualButton.LED_RIGHT, led_r)
#         # exit program
#
#         face_recognition_running = False
#
#     if not process:
#         if button_l == DualButton.BUTTON_STATE_PRESSED:
#             led_l = DualButton.LED_STATE_ON
#             db.set_selected_led_state(DualButton.LED_LEFT, led_l)
#             face_recognition_state = True
#         else:
#             led_l = DualButton.LED_STATE_OFF
#             db.set_selected_led_state(DualButton.LED_LEFT, led_l)
#             face_recognition_state = False

            #print "face_state = "+str(face_recognition_state)+"\nface_running: " + str(face_recognition_running) + "\nprocess: "+str(process)+"\n---"

# def profile_process(cb, profile_name):
# EventLogger.debug("profile_process started--------------")
#     msg = "Working... as intended!"
#
#     if not profile_name or profile_name == "":
#         msg = "No Profile Name was given!"
#         EventLogger.error(msg)
#         cb(msg)
#
#     else:
#         global profiler
#         #TODO remove mode, when?
#         msg = profiler.start_profile_routine(profile_name)
#         cb(msg)
#
# def callback_profile_process(msg):
#     #TODO give the user the messages?
#     EventLogger.debug("callback_profile_process started-----")
#     EventLogger.debug("callback_profile_process MSG: " + str(msg))
#     EventLogger.debug("callback_profile_process finished----")


#lock = allocate_lock()

# def look_for_face():
# face_detection_webcam(found_face)

# def found_face(frame, faces):
# global face_recognition_state, process
#
#     if frame is None or faces is None:
#         print "found_face: one param is None"
#
#     max = len(faces)
#     print "Found " + str(len(faces)) + " images"
#
#     # process the faces
#     for i, val in enumerate(faces):
#         rnd = str(randint(0,1000000))
#         # 'cv2.cv.cvmat'
#         util.save_image("./image_" + str(i) + "_" + str(rnd) + ".pgm", val)
#         #util.save_image("./frame_" + str(rnd) + ".jpeg", (cv2.cv.fromarray(frame)))
#         #util.show_image("Face", val )
#
#
#     # FIXME: same face as last frame
#     # Eigenfaces/Fishfaces
#
#     # global process
#     print "finished"
#     db.set_selected_led_state(DualButton.LED_LEFT, DualButton.LED_STATE_OFF)
#     face_recognition_state = False
#     process = False
#
#     start_new_thread(profile_process, (callback_profile_process, "test", ))


if __name__ == '__main__':

    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))

    # ipcon = IPConnection()
    # db = DualButton(DB_UID, ipcon)
    #
    # try:
    # ipcon.connect(HOST, PORT)
    # except Exception as e:
    #     EventLogger.critical("A critical error occur: " + str(e))
    #     sys.exit(1)

    # init values
    # db.set_selected_led_state(DualButton.LED_LEFT, DualButton.LED_STATE_OFF)
    # db.set_selected_led_state(DualButton.LED_RIGHT, DualButton.LED_STATE_ON)
    # db.register_callback(db.CALLBACK_STATE_CHANGED, __cb_state_changed)

    gui = GuiControl.Instance()
    gui.start_ipcon()

    r = TestRecognizer()
    r.recognize(None)

    #r = FaceRecognizer(None)
    # r.recognize([None, 3])

    # if len(sys.argv) != 2:
    #     EventLogger.error("Please start this Program with the parameter 1 or 0")
    #
    # if sys.argv[1] == "1":#------------------------------------------------| Create_Database_Mode
    #     EventLogger.info("Start Mode 1: Create Face Database")
    #     fdb = gfd.GenerateFaceDatabase("Roland")
    #     fdb.generate_face_database()
    #
    # elif sys.argv[1] == "2":#------------------------------------------------| Face_Recognition_Mode
    #     EventLogger.info("Start Mode 2: Face Recognition")
    #     fr_instance = fre.faceRecognitionEigenfaces()
    #     fr_instance.start_process()
    #
    # else:#-----------------------------------------------------------------| Face_Detection_Mode
    #     EventLogger.info("Start Mode default: Detecting Faces")
    #     try:
    #         process = False
    #         #print "face_state = " + str(face_recognition_state) + "\nface_running: " + str( face_recognition_running) + "\nprocess: " + str(process) + "\n---"
    #         while face_recognition_running:
    #             if not process and face_recognition_state:
    #                 lock.acquire()
    #                 process = True
    #                 lock.release()
    #
    #                 print "STARTED"
    #                 start_new_thread(face_detection_webcam, (found_face,))
    #
    #         raise KeyboardInterrupt
    #
    #     except KeyboardInterrupt:
    #         EventLogger.info("Will now end this program")

    # db.set_selected_led_state(DualButton.LED_LEFT, DualButton.LED_STATE_OFF)
    # db.set_selected_led_state(DualButton.LED_RIGHT, DualButton.LED_STATE_OFF)
    #
    # ipcon.disconnect()