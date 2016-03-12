__author__ = 'sunary'


import cv2
import numpy as np


bit_images = []
shape = (40, 100)


def load_image(files_number):
    for f in files_number:
        img = cv2.imread(f, cv2.THRESH_BINARY)
        img = cv2.resize(img, shape)
        img = (img < 128)
        bit_images.append(img)


def get_number(img):
    img = cv2.resize(img, shape)
    img = (img < 128)
    num_point_match = np.zeros(10)
    for i in range(10):
        num_point_match[i] = -np.sum(np.logical_xor(img, bit_images[i]))

    return np.argmax(num_point_match)