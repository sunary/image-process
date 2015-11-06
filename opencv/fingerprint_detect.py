__author__ = 'sunary'


from utils import helper
import os
import cv2
import numpy as np
from pre_process.edge_detect import EdgeDetect


class FingerprintDetect():

    def __init__(self):
        pass

    def process(self, img_file):
        edge_detect = EdgeDetect()
        pix = cv2.imread(os.path.dirname(__file__) + img_file, 0)
        # pix = helper.read_image(os.path.dirname(__file__) + img_file)
        # pix = helper.convert_gray(pix)
        # pix = np.array(pix)

        pix_none = pix.T
        helper.save_image(pix_none, os.path.dirname(__file__) + '/../resources/gray2.png', True)
        pix_none = edge_detect.process(pix_none)
        helper.save_image(pix_none, os.path.dirname(__file__) + '/../resources/edg2e.png')

        # equalize histogram
        pix_equal = cv2.equalizeHist(pix.T)
        helper.save_image(pix_equal, os.path.dirname(__file__) + '/../resources/gray_equal2.png', True)
        pix_equal = edge_detect.process(pix_equal)
        helper.save_image(pix_equal, os.path.dirname(__file__) + '/../resources/edge_equal2.png')

        # Contrast Limited Adaptive Histogram Equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        pix_clahe = clahe.apply(pix.T)
        helper.save_image(pix_clahe, os.path.dirname(__file__) + '/../resources/gray_clahe2.png', True)
        pix_clahe = edge_detect.process(pix_clahe)
        helper.save_image(pix_clahe, os.path.dirname(__file__) + '/../resources/edge_clahe2.png')


if __name__ == '__main__':
    fp_detect = FingerprintDetect()
    pix = fp_detect.process('/../resources/fp02.jpg')