from thread import start_new_thread, allocate_lock
from random import randint
import sys

# own imports
from FaceDetectionWebcam import *
import GenerateFaceDatabase as gfd
import Utilities as util


progess = False
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

    global progess
    progess = False


if __name__ == '__main__':
    if sys.argv[1] == "1":#------------------------------------------------| Create_Database_Mode
        fdb = gfd.GenerateFaceDatabase("Roland")
        fdb.generate_face_database()

    else:#-----------------------------------------------------------------| Face_Detection_Mode
        try:
            progess = False
            while True:
                if not progess:
                    lock.acquire()
                    progess = True
                    lock.release()

                    progess = start_new_thread(face_detection_webcam, (found_face,))

        except KeyboardInterrupt:
            print "Will now end this program"

    end_webcam()