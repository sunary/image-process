__author__ = 'sunary'


import cv2
import numpy as np


def ostu_algorithm(img, blursize):
    blur = cv2.GaussianBlur(img, (blursize, blursize), 0)
    hist = cv2.calcHist([blur], [0], None, [256], [0, 256])
    hist_norm = hist.ravel()/hist.max()
    Q = hist_norm.cumsum()
    bins = np.arange(256)
    fn_min = np.inf
    thresh = -1
    for i in xrange(1, 256):
        p1, p2 = np.hsplit(hist_norm, [i]) # probabilities
        q1, q2 = Q[i], Q[255] - Q[i] # cum sum of classes
        b1, b2 = np.hsplit(bins, [i]) # weights

        if q1 == 0: continue
        if q2 == 0: continue
        m1, m2 = np.sum(p1 * b1)/q1, np.sum(p2 * b2)/q2
        v1, v2 = np.sum(((b1 - m1) **2)*p1)/q1, np.sum(((b2 - m2) **2) *p2)/q2
        fn = v1*q1 + v2*q2

        if fn < fn_min:
            fn_min = fn
            thresh = i
    ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return otsu