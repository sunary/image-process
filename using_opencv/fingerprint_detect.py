__author__ = 'sunary'


import os
import cv2
import numpy as np
from preprocess import edge_detect
from preprocess import histogram_equalization
from preprocess.gabor_filter import GaborFilter


class FingerprintDetect():

    def __init__(self):
        pass

    def convert_gray(self, img_file):
        pix = cv2.imread(os.path.dirname(__file__) + img_file, 0)

        pix_none = pix
        pix_none = edge_detect.edge_detect(pix_none)
        cv2.imshow('pix-none', np.array(pix_none))

        # equalize histogram
        pix_equal = cv2.equalizeHist(pix)
        pix_equal = edge_detect.edge_detect(pix_equal)
        cv2.imshow('pix-equal', np.array(pix_equal))

        # Contrast Limited Adaptive Histogram Equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
        pix_clahe = clahe.apply(pix)
        cv2.imshow('pix-clahe-gray', np.array(pix_clahe))

        pix_threshold = cv2.adaptiveThreshold(np.array(pix_clahe) , 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)
        cv2.imshow('pix-threshold', pix_threshold)

        pix_clahe = edge_detect.edge_detect(pix_clahe)
        cv2.imshow('pix-clahe', np.array(pix_clahe))

        cv2.waitKey()

    def convert_hsv(self, img_file):
        pix = cv2.imread(os.path.dirname(__file__) + img_file)

        r_size = 5
        c_size = r_size - 1

        # using HSV space
        hsv = cv2.cvtColor(pix, cv2.COLOR_BGR2HLS)
        pix_s = hsv[:, :, 1]
        cv2.imshow('pix-s', pix_s)
        # Adaptive Threshold -> CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(c_size, c_size))
        pix_clahe = clahe.apply(pix_s)
        pix_bin = cv2.adaptiveThreshold(pix_clahe, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,
                                        blockSize=r_size*2 + 1, C=r_size)
        cv2.imshow('pix-bin', pix_bin)
        pix_threshold = histogram_equalization.ostu_algorithm(pix_bin, r_size - 2)
        cv2.imshow('pix-ostu', pix_threshold)

        # fe = FingerprintEnhance()
        # pix_enhance = fe.gabor_filter(pix_threshold)
        # cv2.imshow("pix-enhance", np.array(pix_enhance))

        gabor = GaborFilter()
        pix_gabor = gabor.process(pix_threshold)
        cv2.imshow("pix-gabor", np.array(pix_gabor))

        cv2.waitKey()

if __name__ == '__main__':
    fp_detect = FingerprintDetect()
    # fp_detect.convert_gray('/../resources/fp03.jpg')
    fp_detect.convert_hsv('/../resources/fp03.jpg')