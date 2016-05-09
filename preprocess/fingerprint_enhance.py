__author__ = 'sunary'


import math
import numpy as np


class FingerprintEnhance():

    def __init__(self):
        pass

    def gabor_filter(self, pix):
        print("fingerprint enhance calculator")
        block_size = (9, 9)

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
                min_i, max_i, min_j, max_j = self.ij_value((len(pix), len(pix[0])), block_size, i, j)

                _vx = vx_integral_img[max_i][max_j] + vx_integral_img[min_i][min_j] -\
                      (vx_integral_img[max_i][min_j] + vx_integral_img[min_i][max_j])
                _vy = vy_integral_img[max_i][max_j] + vy_integral_img[min_i][min_j] -\
                      (vy_integral_img[max_i][min_j] + vy_integral_img[min_i][max_j])

                orientation[i][j] = math.atan2(_vy, _vx)/2

        integral_orientation = self.cal_integral_img(orientation)
        mean_orientation = [[0] * len(pix[0]) for _ in range(len(pix))]
        for i in range(len(pix)):
            for j in range(len(pix[0])):
                min_i, max_i, min_j, max_j = self.ij_value((len(pix), len(pix[0])), block_size, i, j)

                mean_orientation[i][j] = 1.*(integral_orientation[max_i][max_j] + integral_orientation[min_i][min_j] -\
                      (integral_orientation[max_i][min_j] + integral_orientation[min_i][max_j]))/\
                      (block_size[0] * block_size[1])

        variance_orientation = [[0] * len(pix[0]) for _ in range(len(pix))]
        for i in range(block_size[0]/2, len(pix) - block_size[0]/2):
            for j in range(block_size[1]/2, len(pix[0]) - block_size[1]/2):

                for m in range(-block_size[0]/2, block_size[0]/2 + 1):
                    for n in range(-block_size[1]/2, block_size[1]/2 + 1):
                        variance_orientation[i][j] += (mean_orientation[i][j] - orientation[i + m][j + n])**2

                variance_orientation[i][j] = math.sqrt(variance_orientation[i][j] / (block_size[0] * block_size[1]))

        confident = [[0] * len(pix[0]) for _ in range(len(pix))]
        gen_pix = [[0xffffff] * len(pix[0]) for _ in range(len(pix))]
        threshold = 0
        conf_stat = []
        for i in range(block_size[0]/2, len(pix) - block_size[0]/2):
            for j in range(block_size[1]/2, len(pix[0]) - block_size[1]/2):
                min_i, max_i, min_j, max_j = self.ij_value((len(pix), len(pix[0])), block_size, i, j)

                dx = vx_integral_img[max_i][max_j] + vx_integral_img[min_i][min_j] -\
                      (vx_integral_img[max_i][min_j] + vx_integral_img[min_i][max_j])
                dy = vy_integral_img[max_i][max_j] + vy_integral_img[min_i][min_j] -\
                      (vy_integral_img[max_i][min_j] + vy_integral_img[min_i][max_j])

                memx = memy = 0

                for _ in range(block_size[0]/2):
                    confident[i][j] += self.gaussian_dist_angle(orientation[i + memx][j + memy], mean_orientation[i][j], variance_orientation[i][j])
                    confident[i][j] += self.gaussian_dist_angle(orientation[i - memx][j - memy], mean_orientation[i][j], variance_orientation[i][j])
                    confident[i][j] -= self.gaussian_dist_angle(orientation[i + memx][j - memy], mean_orientation[i][j], variance_orientation[i][j])
                    confident[i][j] -= self.gaussian_dist_angle(orientation[i - memx][j + memy], mean_orientation[i][j], variance_orientation[i][j])

                    if dx*memy < dy*memx:
                        memy += 1
                    else:
                        memx += 1

                conf_stat.append(confident[i][j])
                if confident[i][j] > threshold:
                    gen_pix[i][j] = 0

        print np.histogram(conf_stat, 30)

        return gen_pix

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

    def orientation_field(self, pix):
        block_size = (15, 15)

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

        orientation = [[0] * len(pix[0]) for _ in range(len(pix))]
        block_orientation = [[0] * n_blocks_y for _ in range(n_blocks_x)]
        block_variance = [[0] * n_blocks_y for _ in range(n_blocks_x)]

        for i in range(block_size[0]/2, len(pix) - block_size[0]/2):
            for j in range(block_size[1]/2, len(pix[0]) - block_size[1]/2):
                sum_v1 = 0.0
                sum_v2 = 0.0

                for ii in range(-block_size[0]/2, block_size[0]/2 + 1):
                    for jj in range(-block_size[1]/2, block_size[1]/2 + 1):
                        sum_v1 += 2 * vx[i + ii][j + jj] * vy[i + ii][j + jj]
                        sum_v2 += vx[i + ii][j + jj] **2 - vy[i + ii][j + jj] **2

                orientation[i][j] = math.atan2(sum_v2, sum_v1)/2

        for m in range(len(block_orientation)):
            for n in range(len(block_orientation[0])):
                sum_v1 = 0.0
                sum_v2 = 0.0

                values = []
                for i in range(block_size[0]):
                    for j in range(block_size[1]):
                        pix_i = min(m * len(block_orientation) + i, len(pix) - 1)
                        pix_j = min(n * len(block_orientation[0]) + j, len(pix[0]) - 1)

                        sum_v1 += 2 * vx[pix_i][pix_j] * vy[pix_i][pix_j]
                        sum_v2 += vx[pix_i][pix_j] **2 - vy[pix_i][pix_j] **2
                        values.append(orientation[m + i][n + j])

                block_orientation[m][n] = math.atan2(sum_v2, sum_v1)/2
                curr_var = 0
                for phi in values:
                    curr_var += ((phi - block_orientation[m][n] + 10 * math.pi) % math.pi) **2
                block_variance[m][n] = curr_var

        gen_pix = [[0xffffff] * len(pix[0]) for _ in range(len(pix))]
        threshold = 0.02

        ht_stat = []
        hb_stat = []
        value_Y = 100
        for ii in range(len(pix)):
            for jj in range(len(pix[0])):
                m = min(ii / block_size[0], len(block_orientation) - 1)
                n = min(jj / block_size[1], len(block_orientation[1]) - 1)

                ro = [-math.sin(block_orientation[m][n])/2, math.sin(block_orientation[m][n])/2]
                i = value_Y * ro[0]
                j = value_Y * ro[1]
                d = value_Y / (2* math.cos(block_orientation[m][n]))

                l = int(j * math.tan(block_orientation[m][n]) + .5)
                delta = block_variance[m][n]
                ht = 0
                hb = 0

                if i == l:
                    ht = self.gaussian_dist(delta)
                elif i == l - d:
                    ht = -self.gaussian_dist(delta)

                if i == l:
                    hb = self.gaussian_dist(delta)
                elif i == l + d:
                    hb = -self.gaussian_dist(delta)

                if ht >= threshold and hb >= threshold:
                    gen_pix[ii][jj] = 0

                ht_stat.append(ht)
                hb_stat.append(hb)

        print np.histogram(ht_stat, 30)
        print np.histogram(ht_stat, 30)

        return gen_pix

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

    def gaussian_dist(self, x, mx=0, vx=1):
        return math.exp(-.5 * ((x - mx) / vx) **2)

    def gaussian_dist_angle(self, x, mx=0, vx=1):
        x = x - mx
        if x < math.pi:
            x += 2 * math.pi
        if x > math.pi:
            x -= 2 * math.pi
        return math.exp(-.5 * ((x - mx) / vx) **2)


if __name__ == '__main__':
    fp = FingerprintEnhance()
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
    print fp.gabor_filter(pix)