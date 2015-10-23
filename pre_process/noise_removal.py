__author__ = 'sunary'


import math


class NoiseRemoval():

    def __init__(self):
        self.load_mask()

    def load_mask(self, mask=None):
        self.mask = [[1, 1, 1],
                     [1, 1, 1],
                     [1, 1, 1]]

        self.mask = [[1, 2, 1],
                     [2, 4, 2],
                     [1, 2, 1]]

        self.mask = mask or self.mask
        self.sum = sum([sum(i) for i in self.mask])

    def process(self, pix, median=True):
        '''
        Median method
        '''
        pix_removal = [[0]* len(pix[0]) for _ in range(len(pix))]

        for i in range(len(pix_removal)):
            pix_removal[i][0] = pix[i][0]
            pix_removal[i][len(pix_removal[0]) - 1] = pix[i][len([pix[0]]) - 1]

        for j in range(len(pix_removal[0])):
            pix_removal[0][j] = pix[0][j]
            pix_removal[len(pix_removal[0]) - 1][j] = pix[len(pix[0]) - 1][j]

        for i in range(len(self.mask)/2, len(pix) - len(self.mask)/2):
            for j in range(len(self.mask)/2, len(pix[0]) - len(self.mask)/2):
                for mi in range(len(self.mask)):
                    for mj in range(len(self.mask)):
                        pix_removal[i][j] += self.mask[mi][mj] * pix[i + mi - len(self.mask)/2][j + mj - len(self.mask)/2]

                pix_removal[i][j] /= self.sum
                if median:
                    median_value = pix[i][j]
                    min_abs = 256
                    for mi in range(len(self.mask)):
                        for mj in range(len(self.mask)):
                            if math.fabs(pix[i + mi - len(self.mask)/2][j + mj - len(self.mask)/2] - pix_removal[i][j]) < min_abs:
                                min_abs = math.fabs(pix[i + mi - len(self.mask)/2][j + mj - len(self.mask)/2] - pix_removal[i][j])
                                median_value = pix[i + mi - len(self.mask)/2][j + mj - len(self.mask)/2]

                    pix_removal[i][j] = median_value

        return pix_removal


if __name__ == '__main__':
    noise_removal = NoiseRemoval()
    pix = [[100, 100, 100, 100, 100,],
           [100, 200, 205, 203, 100,],
           [100, 195, 200, 200, 100,],
           [100, 200, 205, 195, 100,],
           [100, 100, 100, 100, 100,]]
    print noise_removal.process(pix)