__author__ = 'sunary'


import math
import numpy as np
from numpy import unravel_index


class LineDetect():

    def __init__(self):
        self.cos_angle = [math.cos(x * math.pi/180) for x in range(180)]
        self.sin_angle = [math.sin(x * math.pi/180) for x in range(180)]

    def basic(self, pix, binary_image=False):
        width, height = pix.shape[:2]
        if binary_image:
            mean = np.mean(pix)
            pix = [[0 if x < mean else 1 for x in y] for y in pix]

        histogram = [[0]*180 for _ in range(2*(len(pix) + len(pix[0])))]

        for i in range(width):
            for j in range(height):
                if pix[i][j]:
                    for angle in range(180):
                        d = i * self.cos_angle[angle] + j * self.sin_angle[angle]
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

    def process(self, pix, binary_image=False):
        if binary_image:
            mean = np.mean(pix)
            pix = pix > mean

        width, height = pix.shape[:2]
        histogram = np.zeros((2*(width + height), 180))

        for (i, j), value in np.ndenumerate(pix):
            if value:
                for angle in np.arange(180):
                    d = i * self.cos_angle[angle] + j * self.sin_angle[angle]
                    histogram[int(round(d)) + (width + height)][angle] += 1

        max_rate = unravel_index(histogram.argmax(), histogram.shape)

        return max_rate[0] - (width + height), max_rate[1]


if __name__ == '__main__':
    line_detect = LineDetect()
    pix = [[0, 0, 0, 0, 0, 0, 0, 0],
           [1, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 1, 0]]
    print line_detect.basic(pix)