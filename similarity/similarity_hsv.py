__author__ = 'sunary'

import os
import math
from PIL import Image

class SimilarityHSV():

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)

    def read_image(self):
        self.img = Image.open(self.current_dir + '/../resources/flower.jpg')
        data = self.img.getdata()

        self.pix = [[0]*self.img.size[1] for _ in range(self.img.size[0])]
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                self.pix[i][j] = (data[j*self.img.size[0] + i][0], data[j*self.img.size[0] + i][1], data[j*self.img.size[0] + i][2])

    def create_histogram(self):
        self.range_h = 8
        self.range_s = 12
        self.range_v = 3
        self.histogram_hsv = []
        for h in range(self.range_h):
            for s in range(self.range_s):
                for v in range(self.range_v):
                    self.histogram_hsv.append([(h + 1.0)*360/ self.range_h, (s + 1.0)/ self.range_s, (h + 1.0)/ self.range_v])

    def region_computor(self):
        segments = [(0, self.img.size[0]/2, 0, self.img.size[1]/2), (self.img.size[0]/2, self.img.size[0], 0, self.img.size[1]/2),
                    (self.img.size[0]/2, self.img.size[0], self.img.size[1]/2, self.img.size[1]), (0, self.img.size[0]/2, self.img.size[1]/2, self.img.size[1])]
        (axesX, axesY) = (int(self.img.size[0] * 0.75) / 2, int(self.img.size[1] * 0.75) / 2)


    def process(self):
        self.create_histogram()

        histogram = [1]* (self.range_h*self.range_s*self.range_v)

        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                self.pix[i][j] = self._RBG_to_HSV(self.pix[i][j])
                h = 0
                while h < self.range_h:
                    s = 0
                    while s < self.range_s:
                        v = 0
                        while v < self.range_v:
                            if self.pix[i][j][0] <= self.histogram_hsv[h*self.range_s*self.range_v + s*self.range_v + v][0] \
                                and self.pix[i][j][1] <= self.histogram_hsv[h*self.range_s*self.range_v + s*self.range_v + v][1] \
                                    and self.pix[i][j][2] <= self.histogram_hsv[h*self.range_s*self.range_v + s*self.range_v + v][2]:
                                histogram[h*self.range_s*self.range_v + s*self.range_v + v] += 1
                                h, s, v = (self.range_h, self.range_s, self.range_v)
                            v += 1
                        s += 1
                    h += 1

        for i in range(self.range_h*self.range_s*self.range_v):
            histogram[i] *= 1.0/(self.img.size[0]*self.img.size[1])

        print histogram

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
    similarity_HSV.read_image()
    similarity_HSV.process()
