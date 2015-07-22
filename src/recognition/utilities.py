import os
from cv2 import *
from util.event_logger import EventLogger

# Opencv utilities
def save_image(path, image):
    cv.SaveImage(path, image)

def show_image(name, image):
    cv.NamedWindow(name, 1)
    cv.ShowImage(name, image)
    waitKey(0) & 0xFF

# TODO: convertTo pgm tool

# OS utilities
def create_dir(name):
    path = "./faceDatabase/" + name

    if not os.path.exists(path):
        os.makedirs(path)

    return path

def create_csv(basePath):
    SEPARATOR=";"

    label = 0
    for dirname, dirnames, filenames in os.walk(basePath):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s/%s" % (subject_path, filename)
                EventLogger.info(abs_path, SEPARATOR, label)

            label += 1

    #TODO: write the csv to file