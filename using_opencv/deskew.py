__author__ = 'sunary'


import cv2
import numpy as np
from pre_process import histogram_equalization
from pre_process.edge_detect import EdgeDetect
from pre_process.line_detect import LineDetect


def compute_skew(img, is_binary=True, canny=True):
    if not is_binary:
        img = histogram_equalization.ostu_algorithm(img)

    if canny:
        img = auto_canny(img)
    else:
        edge = EdgeDetect()
        img = edge.process(img)

    line = LineDetect()
    angle = line.process(img, binary_image=True)[1]

    angle = -angle if angle < 90 else (180 - angle)
    angle = -(90 - angle) if angle > 45 else angle
    angle = -(90 + angle) if angle < -45 else angle

    return angle


def auto_canny(img, sigma=0.33):
    v = np.median(img)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)

    return edged


def deskew(img, is_binary=True):
    angle = compute_skew(img, is_binary)

    if not angle:
        return img

    image_center = (np.size(img, 1)/2, np.size(img, 0)/2)

    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
    deskewed = cv2.warpAffine(img, rot_mat, (np.size(img, 1), np.size(img, 0)), flags=cv2.INTER_LINEAR)

    if is_binary:
        deskewed = histogram_equalization.binary(deskewed)

    return deskewed
