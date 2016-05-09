__author__ = 'sunary'


import math


class OrientationField():

    def __init__(self):
        pass

    def orientation(self, pix):
        block_size = (9, 9)

        vx = [[0] * len(pix[0]) for _ in range(len(pix))]
        vy = [[0] * len(pix[0]) for _ in range(len(pix))]

        self._sobel()

        for i in range(len(self.gx)/2, len(pix) - len(self.gx)/2):
            for j in range(len(self.gy)/2, len(pix[0]) - len(self.gy)/2):

                for d1 in range(len(self.gx)):
                    for d2 in range(len(self.gx)):
                        vx[i][j] += self.gx[d1][d2] * pix[i + d1 - len(self.gx)/2][j + d2 - len(self.gx)/2]
                        vy[i][j] += self.gy[d1][d2] * pix[i + d1 - len(self.gx)/2][j + d2 - len(self.gy)/2]

        n_blocks_x = len(pix) / block_size[0]
        n_blocks_y = len(pix[0]) / block_size[1]

        block_orientation = [[0] * n_blocks_y for _ in range(n_blocks_x)]

        for i in range(0, n_blocks_x):
            for j in range(0, n_blocks_y):
                sum_v1 = 0.0
                sum_v2 = 0.0

                for ii in range(0, block_size[0]):
                    for jj in range(0, block_size[1]):
                        sum_v1 += 2 * vx[i + ii][j + jj] * vy[i + ii][j + jj]
                        sum_v2 += vx[i + ii][j + jj] **2 - vy[i + ii][j + jj] **2

                block_orientation[i][j] = math.atan2(sum_v2, sum_v1)/2

        return block_orientation

    def _sobel(self):
        self.gx = [[-1, 0, 1],
                  [-2, 0, 2],
                  [-1, 0, 1]]
        self.gy = [[-1, -2, -1],
                  [0, 0, 0],
                  [1, 2, 1]]


if __name__ == '__main__':
    of = OrientationField()
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
    print of.orientation(pix)
