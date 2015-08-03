import os
from cv2 import *
from util.event_logger import EventLogger

# Opencv utilities
def save_image(path, image):
    cv.SaveImage(path, image)

def show_image(name, image):
    cv.NamedWindow(name, 1)
    cv.ShowImage(name, image)
    waitKey(0)

# TODO: convertTo pgm tool

# OS utilities
def create_dir(name):
    path = ".%srecognition%sfaceDatabase%s" + name % (os.sep)

    if not os.path.exists(path):
        os.makedirs(path)

    return path

def get_id_of_index(basePath, index):
    f = open(basePath + "/faces.csv", 'r')
    content = f.readlines()
    user_index = None

    for line in content:
        split = line.split(";")
        path = split[0]
        id = split[1]

        if int(id) == index:
            tmp = path.split(os.sep)
            user_index = tmp[len(tmp) - 2]
            break

    return user_index


def create_csv(basePath):
    EventLogger.info("create_csv: Starting")
    SEPARATOR=";"

    f = open(basePath + "/faces.csv", 'w')

    label = 1
    for dirname, dirnames, filenames in os.walk(basePath):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                abs_path = "%s%s%s" % (subject_path, os.sep, filename)
                f.write(str(abs_path) + " " + str(SEPARATOR) + " " + str(label) + "\n")
            label += 1

    f.close()