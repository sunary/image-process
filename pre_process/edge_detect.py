__author__ = 'sunary'


from pre_process.noise_removal import NoiseRemoval
from utils import helper
import os
import numpy as np


class EdgeDetect():

    def __init__(self):
        pass

    def basic(self, pix):
        temp_x = [[0] * len(pix[0]) for _ in range(len(pix))]
        temp_y = [[0] * len(pix[0]) for _ in range(len(pix))]

        edge_pix = [[0] * len(pix[0]) for _ in range(len(pix))]

        gx, gy = self._sobel()
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

    def process(self, pix):
        temp_x = np.zeros_like(pix)
        temp_y = np.zeros_like(pix)

        sobel = self._sobel()
        gx = np.array(sobel[0])
        gy = np.array(sobel[1])

        for i in np.arange(1, np.size(pix, 0) - 1):
            for j in np.arange(1, np.size(pix, 1) - 1):
                temp_x[i][j] = np.sum(gx * pix[i - 1: i + 2, j - 1: j + 2])
                temp_y[i][j] = np.sum(gy * pix[i - 1: i + 2, j - 1: j + 2])

        sum_square = np.square(temp_x) + np.square(temp_y)
        threshold = 2 * np.mean(sum_square)

        edge_pix = np.zeros_like(pix, dtype=np.uint8)
        for (i, j), value in np.ndenumerate(sum_square):
            edge_pix[i][j] = 0 if value < threshold else 0xffffff

        return edge_pix

    def _sobel(self):
        return ([[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]],
                [[-1, -2, -1],
                [0, 0, 0],
                [1, 2, 1]])

        # return ([[1, 2, 0, -2, -1],
        #         [4, 8, 0, -8, -4],
        #         [6, 12, 0, -12, -6],
        #         [4, 8, 0, -8, -4],
        #         [1, 2, 0, -2, -1]],
        #         [[-1, -4, -6, -4, -1],
        #         [-2, -8, -12, -8, -2],
        #         [0, 0, 0, 0, 0],
        #         [2, 8, 12, 8, 2],
        #         [1, 4, 6, 4, 1]])

    def _robert(self):
        return ([[1, 0],
                [0, -1]],
                [[0, 1],
                [-1, 0]])

    def _prewitt(self):
        return ([[-1, 0, 1],
                [-1, 0, 1],
                [-1, 0, 1]],
                [[-1, -1, -1],
                [0, 0, 0],
                [1, 1, 1]])


if __name__ == '__main__':
    edge_detect = EdgeDetect()
    pix = helper.read_image(os.path.dirname(__file__) + '/../resources/fp01.jpg')
    pix = helper.convert_gray(pix)
    helper.save_image(pix, os.path.dirname(__file__) + '/../resources/gray.png', True)
    pix = edge_detect.basic(pix)
    # noise_removal = NoiseRemoval()
    # pix = noise_removal.opening(pix)
    helper.save_image(pix, os.path.dirname(__file__) + '/../resources/edge.png')