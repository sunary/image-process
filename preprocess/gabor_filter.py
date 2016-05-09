__author__ = 'sunary'


import numpy as np
import math


class GaborFilter():

    def __init__(self):
        self.block_size = (9, 9)

    def process(self, pix):
        block_orientation = self.orientation(pix)
        variance_orientation = self.variance(pix)
        pix = self.gabor_filter(block_orientation, variance_orientation, 5, 0)

        return pix

    def orientation(self, pix):
        vx = [[0] * len(pix[0]) for _ in range(len(pix))]
        vy = [[0] * len(pix[0]) for _ in range(len(pix))]

        self._sobel()

        for i in range(len(self.gx)/2, len(pix) - len(self.gx)/2):
            for j in range(len(self.gy)/2, len(pix[0]) - len(self.gy)/2):

                for d1 in range(len(self.gx)):
                    for d2 in range(len(self.gx)):
                        vx[i][j] += self.gx[d1][d2] * pix[i + d1 - len(self.gx)/2][j + d2 - len(self.gx)/2]
                        vy[i][j] += self.gy[d1][d2] * pix[i + d1 - len(self.gx)/2][j + d2 - len(self.gy)/2]

        n_blocks_x = len(pix) / self.block_size[0]
        n_blocks_y = len(pix[0]) / self.block_size[1]

        block_orientation = [[0] * n_blocks_y for _ in range(n_blocks_x)]

        for i in range(0, n_blocks_x):
            for j in range(0, n_blocks_y):
                sum_v1 = 0.0
                sum_v2 = 0.0

                for ii in range(0, self.block_size[0]):
                    for jj in range(0, self.block_size[1]):
                        sum_v1 += 2 * vx[i + ii][j + jj] * vy[i + ii][j + jj]
                        sum_v2 += vx[i + ii][j + jj] **2 - vy[i + ii][j + jj] **2

                block_orientation[i][j] = math.atan2(sum_v2, sum_v1)/2

        return block_orientation

    def variance(self, pix):
        dx = [[0] * len(pix[0]) for _ in range(len(pix))]
        dy = [[0] * len(pix[0]) for _ in range(len(pix))]

        self._sobel()

        for i in range(len(self.gx)/2, len(pix) - len(self.gx)/2):
            for j in range(len(self.gy)/2, len(pix[0]) - len(self.gy)/2):

                for d1 in range(len(self.gx)):
                    for d2 in range(len(self.gx)):
                        dx[i][j] += self.gx[d1][d2] * pix[i + d1 - len(self.gx)/2][j + d2 - len(self.gx)/2]
                        dy[i][j] += self.gy[d1][d2] * pix[i + d1 - len(self.gx)/2][j + d2 - len(self.gy)/2]

        vx = [[2 * dx[i][j] * dy[i][j] for j in range(len(pix[0]))] for i in range(len(pix))]
        vy = [[dx[i][j]**2 - dy[i][j]**2 for j in range(len(pix[0]))] for i in range(len(pix))]

        vx_integral_img = self.cal_integral_img(vx)
        vy_integral_img = self.cal_integral_img(vy)

        orientation = [[0] * len(pix[0]) for _ in range(len(pix))]
        for i in range(len(pix)):
            for j in range(len(pix[0])):
                min_i, max_i, min_j, max_j = self.ij_value((len(pix), len(pix[0])), self.block_size, i, j)

                _vx = vx_integral_img[max_i][max_j] + vx_integral_img[min_i][min_j] -\
                      (vx_integral_img[max_i][min_j] + vx_integral_img[min_i][max_j])
                _vy = vy_integral_img[max_i][max_j] + vy_integral_img[min_i][min_j] -\
                      (vy_integral_img[max_i][min_j] + vy_integral_img[min_i][max_j])

                orientation[i][j] = math.atan2(_vy, _vx)/2

        integral_orientation = self.cal_integral_img(orientation)
        mean_orientation = [[0] * len(pix[0]) for _ in range(len(pix))]
        for i in range(len(pix)):
            for j in range(len(pix[0])):
                min_i, max_i, min_j, max_j = self.ij_value((len(pix), len(pix[0])), self.block_size, i, j)

                mean_orientation[i][j] = 1.*(integral_orientation[max_i][max_j] + integral_orientation[min_i][min_j] -\
                      (integral_orientation[max_i][min_j] + integral_orientation[min_i][max_j]))/\
                      (self.block_size[0] * self.block_size[1])

        variance_orientation = [[0] * len(pix[0]) for _ in range(len(pix))]
        for i in range(self.block_size[0]/2, len(pix) - self.block_size[0]/2):
            for j in range(self.block_size[1]/2, len(pix[0]) - self.block_size[1]/2):

                for m in range(-self.block_size[0]/2, self.block_size[0]/2 + 1):
                    for n in range(-self.block_size[1]/2, self.block_size[1]/2 + 1):
                        variance_orientation[i][j] += (mean_orientation[i][j] - orientation[i + m][j + n])**2

                variance_orientation[i][j] = math.sqrt(variance_orientation[i][j] / (self.block_size[0] * self.block_size[1]))

        return variance_orientation

    def gabor_filter(self, block_orientation, variance_orientation, wavelength, phase_offset):
        gabor = [[0]*len(variance_orientation[0]) for _ in range(len(variance_orientation))]

        for i in range(len(variance_orientation)/self.block_size[0] * self.block_size[0]):
            for j in range(len(variance_orientation[0])/self.block_size[1] * self.block_size[1]):
                theta = block_orientation[i/self.block_size[0]][j/self.block_size[1]]
                x_theta = i * math.cos(theta) + j * math.sin(theta)
                y_theta = -i * math.sin(theta) + j * math.cos(theta)
                try:
                    gabor[i][j] = math.exp(-(x_theta **2 + (wavelength * y_theta) **2)/(2 * variance_orientation[i][j] **2)) * math.cos(2 * math.pi * x_theta/wavelength + phase_offset)
                except:
                    gabor[i][j] = 0

        return gabor

    def _sobel(self):
        self.gx = [[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]]
        self.gy = [[-1, -2, -1],
                  [0, 0, 0],
                  [1, 2, 1]]

        self.gx = [[1, 2, 0, -2, -1],
                   [4, 8, 0, -8, -4],
                   [6, 12, 0, -12, -6],
                   [4, 8, 0, -8, -4],
                   [1, 2, 0, -2, -1]]
        self.gy = [[-1, -4, -6, -4, -1],
                   [-2, -8, -12, -8, -2],
                   [0, 0, 0, 0, 0],
                   [2, 8, 12, 8, 2],
                   [1, 4, 6, 4, 1]]

    def cal_integral_img(self, pix):
        '''
        Examples:
            >>> cal_integral_img([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
            [[1, 3, 6], [2, 6, 12], [3, 9, 18]]
        '''

        integral_img = [[0] * len(pix[0]) for _ in range(len(pix))]

        integral_img[0][0] = pix[0][0]
        for j in range(1, len(pix[0])):
            integral_img[0][j] = integral_img[0][j - 1] + pix[0][j]

        for i in range(1, len(pix)):
            line_sum = 0
            for j in range(len(pix[0])):
                line_sum += pix[i][j]
                integral_img[i][j] = integral_img[i - 1][j] + line_sum

        return integral_img

    def ij_value(self, pix_size, block_size, i, j):
        min_i = max(i - block_size[0]/2-1, 0)
        max_i = min(i + block_size[0]/2, pix_size[0] - 1)
        min_j = max(j - block_size[1]/2-1, 0)
        max_j = min(j + block_size[1]/2, pix_size[1] - 1)

        return min_i, max_i, min_j, max_j


if __name__ == '__main__':
    gabor_filter = GaborFilter()
    pix = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0],
          [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
          [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
          [0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
          [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]]
    print gabor_filter.process(pix)