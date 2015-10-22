__author__ = 'sunary'


import os
import math
from PIL import Image


class SimilarityHSV():

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.range_hsv = (8, 12, 3)

    def create_histogram(self):
        histogram_hsv = []
        for h in range(self.range_hsv[0]):
            for s in range(self.range_hsv[1]):
                for v in range(self.range_hsv[2]):
                    histogram_hsv.append([(h + 1.0)*360/ self.range_hsv[0], (s + 1.0)/ self.range_hsv[1], (h + 1.0)/ self.range_hsv[2]])

    def region_computor(self):
        return None

    def process(self, pix, histogram_hsv):
        self.create_histogram()

        histogram_vector = [1]* (self.range_hsv[0] * self.range_hsv[1] * self.range_hsv[2])

        for i in range(len(pix)):
            for j in range(len(pix[0])):
                pix[i][j] = self._RBG_to_HSV(pix[i][j])
                h = 0
                while h < self.range_hsv[0]:
                    s = 0
                    while s < self.range_hsv[1]:
                        v = 0
                        while v < self.range_hsv[2]:
                            if pix[i][j][0] <= histogram_hsv[h*self.range_hsv[0]*self.range_hsv[2] + s*self.range_hsv[2] + v][0] \
                                and pix[i][j][1] <= histogram_hsv[h*self.range_hsv[1]*self.range_hsv[2] + s*self.range_hsv[2] + v][1] \
                                    and pix[i][j][2] <= histogram_hsv[h*self.range_hsv[1]*self.range_hsv[2] + s*self.range_hsv[2] + v][2]:
                                histogram_vector[h*self.range_hsv[0]*self.range_hsv[1] + s*self.range_hsv[2] + v] += 1
                                h, s, v = self.range_hsv[0]
                            v += 1
                        s += 1
                    h += 1

        for i in range(self.range_hsv[0] * self.range_hsv[1] * self.range_hsv[2]):
            histogram_vector[i] *= 1.0/(len(pix) * len(pix[0]))

        return histogram_vector

    def chi_squared_distance(self, histogram_x, histogram_y):
        distance = 0
        for i in range(len(histogram_x)):
            distance += (histogram_x[i] - histogram_y[i])*(histogram_x[i] - histogram_y[i])/(histogram_x[i] + histogram_y[i])

        return distance/2

    # [360, 1, 1]
    def _RBG_to_HSV(self, rgb):
        hsv = [0, 0, 0]
        min_c = min(rgb[0], rgb[1], rgb[2])
        max_c = max(rgb[0], rgb[1], rgb[2])

        hsv[2] = max_c/255.0
        delta = max_c - min_c
        if max_c != 0:
            hsv[1] = delta*1.0/max_c
        else:
            return [-1, 0, hsv[2]]

        if delta == 0:
            hsv[0] = 0
            return hsv

        if rgb[0] == max_c:
            hsv[0] = (rgb[1] - rgb[2])/delta
        elif  rgb[1]  == max_c:
            hsv[0] = 2 + (rgb[2] - rgb[0])/delta
        else:
            hsv[0] = 4 + (rgb[0] - rgb[1])/delta

        hsv[0] *= 60
        if hsv[0] < 0:
            hsv[0] += 360

        return hsv

    # [1, 1, 1]
    def _HSV_to_RBG(self, hsv):
        if hsv[1] == 0:
            return [hsv[2], hsv[2], hsv[2]]

        hsv[0] /= 60.0
        i = math.floor(hsv[0])
        f = hsv[0] - i
        p = hsv[2]*(1 - hsv[1])
        q = hsv[2]*(1 - hsv[1]*f)
        t = hsv[2]*(1 - hsv[1]*(1 - f))

        if i == 0:
            rgb = [hsv[2], t, p]
        elif i == 1:
            rgb = [q, hsv[1], p]
        elif i == 2:
            rgb = [p, hsv[2], t]
        elif i == 3:
            rgb = [p, q, hsv[2]]
        elif i == 4:
            rgb = [t, p, hsv[2]]
        else:
            rgb = [hsv[2], p, q]

        return rgb


if __name__ == '__main__':
    similarity_HSV = SimilarityHSV()
    similarity_HSV.create_histogram()
    similarity_HSV.process()
