__author__ = 'sunary'


import math
import os


class OrientationField():

    SIZE_ORIENTATION = (10, 10)

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)

    def process(self, pix):
        temp_x = [[0] * len(pix[0]) for _ in range(len(pix))]
        temp_y = [[0] * len(pix[0]) for _ in range(len(pix))]

        self._sobel()

        for i in range(len(self.gx)/2, len(pix) - len(self.gx)/2):
            for j in range(len(self.gy)/2, len(pix[0]) - len(self.gy)/2):
                for d1 in range(len(self.gx)):
                    for d2 in range(len(self.gx)):
                        temp_x[i][j] += self.gx[d1][d2] * pix[i + d1 - 1][j + d2 -1]
                        temp_y[i][j] += self.gy[d1][d2] * pix[i + d1 - 1][j + d2 -1]

        orient = [[0]* self.SIZE_ORIENTATION[1]]* self.SIZE_ORIENTATION[0]
        coherence = [[0]* self.SIZE_ORIENTATION[1]]* self.SIZE_ORIENTATION[0]
        for m in range(self.SIZE_ORIENTATION[0]):
            for n in range(self.SIZE_ORIENTATION[1]):
                sum_j1 = 0.0
                sum_j2 = 0.0
                sum_j3 = 0.0
                for i in range(len(pix)/self.SIZE_ORIENTATION[0]):
                    for j in range(len(pix[0])/self.SIZE_ORIENTATION[1]):
                        sum_j1 += 2*temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]
                        sum_j2 += temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j] - temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]
                        sum_j3 += temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j] + temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]

                orient[m][n] = math.atan(sum_j1/sum_j2)/2
                coherence[m][n] = math.sqrt(sum_j1*sum_j1 + sum_j2*sum_j2)/sum_j3

        return orient, coherence

    def _sobel(self):
        self.gx = [[-1, 0, 1],
              [-2, 0, 2],
              [-1, 0, 1]]
        self.gy = [[-1, -2, -1],
              [0, 0, 0],
              [1, 2, 1]]


if __name__ == '__main__':
    orientation = OrientationField()
    orientation.process()
