import os
from cv2 import *


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