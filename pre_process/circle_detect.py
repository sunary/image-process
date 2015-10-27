__author__ = 'sunary'


import math

class CircleDetect():

    def __init__(self):
        pass

    def process(self, pix):
        max_r = min(len(pix), len(pix[0]))/2 + 1
        self.histogram = [[[0]* max_r for _ in range(len(pix[0]))] for _ in range(len(pix))]
        for i in range(len(pix)):
            for j in range(len(pix[0])):
                for a in range(len(pix)):
                    for b in range(len(pix[0])):
                        r = int(math.sqrt((i - a)**2 + (j - b)**2))
                        if r and r < max_r:
                            self.histogram[i][j][r] += 1

        max_rate = 0
        save_a = 0
        save_b = 0
        save_r = 0
        for i in range(0, len(self.histogram)):
            for j in range(0, len(self.histogram[0])):
                for r in range(0, len(self.histogram[0][0])):
                    if self.histogram[i][j][r] > max_rate:
                        max_rate = self.histogram[i][j][r]
                        save_a = i
                        save_b = j
                        save_r = r

        return save_a, save_b, save_r


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
    print circle_detect.process(pix)