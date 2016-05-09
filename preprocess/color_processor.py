__author__ = 'sunary'


import cv2
import numpy as np
from preprocess import histogram_equalization


def add_edge(img, color=False):
    height, width = img.shape[:2]

    mask_value = np.array([0, 0, 0]) if color else 0
    img_edge = auto_canny(img)

    for i in np.arange(height):
        for j in np.arange(width):
            if img_edge[i][j] == 255:
                img[i][j] = mask_value

    return img


def auto_canny(img, sigma=0.33):
    v = np.median(img)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)

    return edged


def color_detect(img, lower, upper, hsv=False):

    if hsv:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_white = np.array(lower, dtype=np.uint8)
        upper_white = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_white, upper_white)
    else:
        lower_white = np.array(lower, dtype=np.uint8)
        upper_white = np.array(upper, dtype=np.uint8)

        if len(img.shape) == 3:
            mask = cv2.inRange(img, lower_white, upper_white)
        else:
            mask = cv2.inRange(img, np.mean(lower_white), np.mean(upper_white))

    return mask


def binary_detect(img):
    img = histogram_equalization.normal(img)
    img = histogram_equalization.binary(img)
    return img


def object_detect(img_color, method_id=0):
    '''
    detect car plate
    '''
    if method_id == 0:
        lower = [0, 0, 120]
        upper = [255, 45, 255]
        img_color = add_edge(img_color, color=True)
        cv2.imshow("add border", img_color)
        img = color_detect(img_color, lower, upper, hsv=True)
    elif method_id == 1:
        lower = [175, 175, 175]
        upper = [255, 255, 255]
        img_gray = add_edge(img_color)
        img = color_detect(img_gray, lower, upper)
    elif method_id == 2:
        img = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)
        img = binary_detect(img)

    return img