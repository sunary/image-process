__author__ = 'sunary'


import cv2
from utils import helper
from preprocess import histogram_equalization
import numpy as np


def basic(pix):
    temp_x = [[0] * len(pix[0]) for _ in range(len(pix))]
    temp_y = [[0] * len(pix[0]) for _ in range(len(pix))]

    edge_pix = [[0] * len(pix[0]) for _ in range(len(pix))]

    gx, gy = _sobel()
    sum_gray = 0
    for i in range(len(gx)/2, len(pix) - len(gx)/2):
        for j in range(len(gx)/2, len(pix[0]) - len(gy)/2):
            for d1 in range(len(gx)):
                for d2 in range(len(gx)):
                    temp_x[i][j] += gx[d1][d2] * pix[i + d1 - len(gx)/2][j + d2 - len(gx)/2]
                    temp_y[i][j] += gy[d1][d2] * pix[i + d1 - len(gy)/2][j + d2 - len(gy)/2]
            sum_gray += temp_x[i][j]*temp_x[i][j] + temp_y[i][j]*temp_y[i][j]

    threshold = 3*sum_gray/((len(pix))*len(pix[0]))

    for i in range(0, len(pix) - 0):
        for j in range(0, len(pix[0]) - 0):
            edge_pix[i][j] = 0x000000 if (temp_x[i][j]*temp_x[i][j] + temp_y[i][j]*temp_y[i][j] > threshold) else 0xffffff

    return edge_pix


def edge_detect(img):
    temp_x = np.zeros_like(img)
    temp_y = np.zeros_like(img)

    sobel = _sobel()
    gx = np.array(sobel[0])
    gy = np.array(sobel[1])

    for i in np.arange(1, np.size(img, 0) - 1):
        for j in np.arange(1, np.size(img, 1) - 1):
            temp_x[i][j] = np.sum(gx * img[i - 1: i + 2, j - 1: j + 2])
            temp_y[i][j] = np.sum(gy * img[i - 1: i + 2, j - 1: j + 2])

    sum_square = np.square(temp_x) + np.square(temp_y)
    threshold = 2 * np.mean(sum_square)

    edge_pix = np.zeros_like(img, dtype=np.uint8)
    for (i, j), value in np.ndenumerate(sum_square):
        edge_pix[i][j] = 0 if value < threshold else 0xffffff

    return edge_pix


def auto_canny(img, sigma=0.33):
    v = np.median(img)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)

    return edged


def full_detect(img, is_binary=True, canny=True):
    if not is_binary:
        # img = histogram_equalization.clahe(img)
        img = histogram_equalization.ostu_algorithm(img)

    if canny:
        img = auto_canny(img)
    else:
        img = edge_detect(img)

    return img


def extractEdges(input, cannyThreshold1=50, cannyThreshold2=200, borderApertureSize=3):
    input_gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    input_gray = cv2.createCLAHE(clipLimit=4.5, tileGridSize=(9,9)).apply(input_gray)
    input_gray = cv2.GaussianBlur(input_gray, (3,3), 1)
    return cv2.Canny(input_gray, cannyThreshold1, cannyThreshold2, apertureSize=borderApertureSize, L2gradient=False)


def _sobel():
    return ([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
            [[-1, -2, -1], [0, 0, 0], [1, 2, 1]])


def _robert(self):
    return ([[1, 0], [0, -1]],
            [[0, 1], [-1, 0]])


def _prewitt(self):
    return ([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]],
            [[-1, -1, -1], [0, 0, 0], [1, 1, 1]])


def bounding_box(img, range_w=None, range_h=None):
    img = histogram_equalization.adaptive_mean(img)
    cv2.imshow('binary', img)

    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
    boundings = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if (not range_w or (w >= range_w[0] and w <= range_w[1])) and \
                (not range_h or (h >= range_h[0] and h <= range_h[1])):
            boundings.append((x, y, w, h))
            cv2.rectangle(img, (x, y), (x + w, y + h), (255), 2)

    return img, boundings


if __name__ == '__main__':
    pix = helper.read_image('../resources/fp01.jpg')
    pix = helper.convert_gray(pix)
    helper.save_image('../resources/gray.png', True)
    pix = basic(pix)
    # noise_removal = NoiseRemoval()
    # pix = noise_removal.opening(pix)
    helper.save_image(pix, '../resources/edge.png')