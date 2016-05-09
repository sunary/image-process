__author__ = 'sunary'


import math
import cv2
import numpy as np


range_angle = 180
cos_angle = [math.cos(x * math.pi/180) for x in range(range_angle)]
sin_angle = [math.sin(x * math.pi/180) for x in range(range_angle)]

def basic(pix, binary_image=False):
    width, height = pix.shape[:2]
    if binary_image:
        mean = np.mean(pix)
        pix = [[0 if x < mean else 1 for x in y] for y in pix]

    histogram = [[0] * range_angle for _ in range(2*(len(pix) + len(pix[0])))]

    for i in range(width):
        for j in range(height):
            if pix[i][j]:
                for angle in range(range_angle):
                    d = i * cos_angle[angle] + j * sin_angle[angle]
                    histogram[int(round(d)) + (width + height)][angle] += 1

    max_rate = 0
    save_r = 0
    save_angle = 0
    for i in range(np.size(histogram, 0)):
        for j in range(np.size(histogram, 1)):
            if histogram[i][j] > max_rate:
                max_rate = histogram[i][j]
                save_r = i
                save_angle = j

    # y = -cos(a)*x/sin(a) + r/sin(a)
    return save_r - (len(pix) + len(pix[0])), save_angle


def process(img, binary_image=False):
    if binary_image:
        mean = np.mean(img)
        img = img > mean

    width, height = img.shape[:2]
    histogram = np.zeros((2*(width + height), range_angle))

    for (i, j), value in np.ndenumerate(img):
        if value:
            for angle in np.arange(range_angle):
                d = i * cos_angle[angle] + j * sin_angle[angle]
                histogram[int(round(d)) + (width + height)][angle] += 1

    max_rate = np.unravel_index(histogram.argmax(), histogram.shape)
    return max_rate[0] - (width + height), max_rate[1]


def houghlines(img, binary_image=True):
    if not binary_image:
        img = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLines(img, 1, np.pi/180, 200)

    if lines is None:
        return 0

    angles = []
    for rho, theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        angles.append(get_angle(x1, y1, x2, y2))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return np.mean(angles)*180/math.pi


def get_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


if __name__ == '__main__':
    pix = [[0, 0, 0, 0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 1, 0]]
    print basic(pix)