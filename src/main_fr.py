from thread import start_new_thread, allocate_lock
from random import randint
import sys

# own imports
from recognition.faceDetectionWebcam import *
import recognition.generateFaceDatabase as gfd
import recognition.faceRecognitionEigenfaces as fre
import recognition.utilities as util
from util.event_logger import EventLogger, ConsoleLogger

process = False
lock = allocate_lock()

def look_for_face():
    face_detection_webcam(found_face)

def found_face(frame, faces):
    if frame is None or faces is None:
        print "found_face: one param is None"

    max = len(faces)
    print "Found " + str(len(faces)) + " images"

    # process the faces
    for i, val in enumerate(faces):
        rnd = str(randint(0,1000000))
        # 'cv2.cv.cvmat'
        util.save_image("./image_" + str(i) + "_" + str(rnd) + ".pgm", val)
        #util.save_image("./frame_" + str(rnd) + ".jpeg", (cv2.cv.fromarray(frame)))
        util.show_image("Face", val )


    # FIXME: same face as last frame
    # Eigenfaces/Fishfaces

    global process
    process = False


if __name__ == '__main__':
    EventLogger.add_logger(ConsoleLogger("ConsoleLogger", EventLogger.EVENT_LOG_LEVEL))

    if len(sys.argv) != 2:
        EventLogger.error("Please start this Program with the parameter 1 or 0")

    if sys.argv[1] == "1":#------------------------------------------------| Create_Database_Mode
        EventLogger.info("Start Mode 1: Create Face Database")
        fdb = gfd.GenerateFaceDatabase("Roland")
        fdb.generate_face_database()

    elif sys.argv[1] == "2":#------------------------------------------------| Face_Recognition_Mode
        EventLogger.info("Start Mode 2: Face Recognition")
        fr_instance = fre.faceRecognitionEigenfaces()
        fr_instance.start_process()

    else:#-----------------------------------------------------------------| Face_Detection_Mode
        EventLogger.info("Start Mode default: Detecting Faces")
        try:
            process = False
            while True:
                if not process:
                    lock.acquire()
                    process = True
                    lock.release()

                    process = start_new_thread(face_detection_webcam, (found_face,))

        except KeyboardInterrupt:
            EventLogger.info("Will now end this program")
        finally:
            end_webcam()