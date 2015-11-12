__author__ = 'sunary'


from utils import helper
import os
import cv2
import numpy as np
from pre_process.edge_detect import EdgeDetect
from pre_process.orientation_field import OrientationField


class FingerprintDetect():

    def __init__(self):
        pass

    def convert_gray(self, img_file):
        edge_detect = EdgeDetect()
        pix = cv2.imread(os.path.dirname(__file__) + img_file, 0)

        pix_none = pix
        pix_none = edge_detect.process(pix_none)
        cv2.imshow('pix-none', np.array(pix_none))

        # equalize histogram
        pix_equal = cv2.equalizeHist(pix)
        pix_equal = edge_detect.process(pix_equal)
        cv2.imshow('pix-equal', np.array(pix_equal))

        # Contrast Limited Adaptive Histogram Equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        pix_clahe = clahe.apply(pix)
        cv2.imshow('pix-clahe-gray', np.array(pix_clahe))

        pix_threshold = cv2.adaptiveThreshold(np.array(pix_clahe) , 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)
        cv2.imshow('pix-threshold', pix_threshold)

        pix_clahe = edge_detect.process(pix_clahe)
        cv2.imshow('pix-clahe', np.array(pix_clahe))

        cv2.waitKey()

    def convert_hsv(self, img_file):
        pix = cv2.imread(os.path.dirname(__file__) + img_file)

        # using HSV space
        hsv = cv2.cvtColor(pix, cv2.COLOR_BGR2HSV)
        pix_s = hsv[:, :, 1]
        # cv2.imshow('pix-s', pix_s)

        # Adaptive Threshold -> CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        pix_clahe = clahe.apply(pix_s)
        pix_threshold = cv2.adaptiveThreshold(pix_clahe , 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)
        cv2.imshow('pix-clare-4', pix_threshold)

        orientation = OrientationField()
        pix_enhance = orientation.fingerprint_enhance(pix_threshold)
        cv2.imshow("pix-enhance", np.array(pix_enhance))

        cv2.waitKey()

if __name__ == '__main__':
    fp_detect = FingerprintDetect()
    # fp_detect.convert_gray('/../resources/fp02.jpg')
    fp_detect.convert_hsv('/../resources/fp02.jpg')