__author__ = 'sunary'


import math


class CircleDetect():

    def __init__(self):
        pass

    def basic(self, pix):
        max_r = min(len(pix), len(pix[0]))/2 + 1
        histogram = [[[0]* max_r for _ in range(len(pix[0]))] for _ in range(len(pix))]

        for i in range(len(pix)):
            for j in range(len(pix[0])):
                for a in range(i, len(pix)):
                    for b in range(j, len(pix[0])):
                        r = int(round(math.sqrt((i - a)**2 + (j - b)**2)))
                        if r and r < max_r:
                            histogram[i][j][r] += 1

        max_rate = 0
        save_a = 0
        save_b = 0
        save_r = 0
        for i in range(len(histogram)):
            for j in range(len(histogram[0])):
                for r in range(len(histogram[0][0])):
                    if histogram[i][j][r] > max_rate:
                        max_rate = histogram[i][j][r]
                        save_a = i
                        save_b = j
                        save_r = r

        #(x - a)^2 + (y - b)^2 = r^2
        return save_a, save_b, save_r

    def process(self, pix):
        pass



if __name__ == '__main__':
    circle_detect = CircleDetect()
    pix = [[0, 0, 1, 0, 0, 0, 0, 0],
           [0, 1, 0, 1, 0, 0, 0, 0],
           [1, 1, 0, 1, 0, 0, 0, 0],
           [0, 1, 0, 1, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]]
    print circle_detect.basic(pix)