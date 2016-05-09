__author__ = 'sunary'


import cv2
import numpy as np
from preprocess import histogram_equalization, edge_detect, line_detect


def compute_skew(img, is_binary=True, canny=True):
    img = edge_detect.full_detect(img, is_binary, canny)

    angle = line_detect.process(img, binary_image=True)[1]
    # angle = line_detect.houghlines(img, binary_image=True)

    angle = -angle if angle < 90 else (180 - angle)
    angle = -(90 - angle) if angle > 45 else angle
    angle = -(90 + angle) if angle < -45 else angle

    return angle


def deskew(img, angle=None, is_binary=True):
    angle = angle or compute_skew(img, is_binary)

    if not angle:
        return img

    image_center = (np.size(img, 1)/2, np.size(img, 0)/2)

    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
    deskewed = cv2.warpAffine(img, rot_mat, (np.size(img, 1), np.size(img, 0)), flags=cv2.INTER_LINEAR)

    if is_binary:
        deskewed = histogram_equalization.binary(deskewed)

    return deskewed
