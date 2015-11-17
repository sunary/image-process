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

    def ostu_threshold(self, img, blursize):
        blur = cv2.GaussianBlur(img,(blursize,blursize),0)
        hist = cv2.calcHist([blur],[0],None,[256],[0,256])
        hist_norm = hist.ravel()/hist.max()
        Q = hist_norm.cumsum()
        bins = np.arange(256)
        fn_min = np.inf
        thresh = -1
        for i in xrange(1,256):
            p1,p2 = np.hsplit(hist_norm,[i]) # probabilities
            q1,q2 = Q[i],Q[255]-Q[i] # cum sum of classes
            b1,b2 = np.hsplit(bins,[i]) # weights
            if q1==0: continue
            if q2==0: continue
            m1,m2 = np.sum(p1*b1)/q1, np.sum(p2*b2)/q2
            v1,v2 = np.sum(((b1-m1)**2)*p1)/q1,np.sum(((b2-m2)**2)*p2)/q2
            fn = v1*q1 + v2*q2
            if fn < fn_min:
                fn_min = fn
                thresh = i
        ret, otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return otsu

    def convert_hsv(self, img_file):
        pix = cv2.imread(os.path.dirname(__file__) + img_file)

        r_size = 5
        c_size = r_size - 1

        # using HSV space
        hsv = cv2.cvtColor(pix, cv2.COLOR_BGR2HSV)
        pix_s = hsv[:, :, 1]
        cv2.imshow('pix-s', pix_s)
        # Adaptive Threshold -> CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(c_size, c_size))
        pix_clahe = clahe.apply(pix_s)
        pix_bin = cv2.adaptiveThreshold(pix_clahe, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                        blockSize=r_size*2 + 1, C=r_size)
        cv2.imshow('pix-bin', pix_bin)
        pix_threshold = self.ostu_threshold(pix_bin, r_size - 2)
        cv2.imshow('pix-ostu', pix_threshold)

        # orientation = OrientationField()
        # pix_enhance = orientation.fingerprint_enhance(pix_threshold)
        # cv2.imshow("pix-enhance", np.array(pix_enhance))

        cv2.waitKey()

if __name__ == '__main__':
    fp_detect = FingerprintDetect()
    # fp_detect.convert_gray('/../resources/fp02.jpg')
    fp_detect.convert_hsv('/../resources/fp02.jpg')