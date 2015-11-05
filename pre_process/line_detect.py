__author__ = 'sunary'


import math


class LineDetect():

    def __init__(self):
        self.cos_angle = [math.cos(x * math.pi/180) for x in range(180)]
        self.sin_angle = [math.sin(x * math.pi/180) for x in range(180)]

    def process(self, pix):
        self.histogram = [[0]*180 for _ in range(2*(len(pix) + len(pix[0])))]

        for i in range(len(pix)):
            for j in range(len(pix[0])):
                if pix[i][j]:
                    for angle in range(180):
                        d = i * self.cos_angle[angle] + j * self.sin_angle[angle]
                        self.histogram[int(round(d)) + (len(pix) + len(pix[0]))][angle] += 1

        max_rate = 0
        save_r = 0
        save_angle = 0
        for i in range(len(self.histogram)):
            for j in range(len(self.histogram[0])):
                if self.histogram[i][j] > max_rate:
                    max_rate = self.histogram[i][j]
                    save_r = i
                    save_angle = j

        # y = -cos(a)*x/sin(a) + r/sin(a)
        return save_r - (len(pix) + len(pix[0])), save_angle


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
    print line_detect.process(pix)