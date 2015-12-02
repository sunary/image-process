__author__ = 'sunary'


import math
from utils import helper
from morphology.morphology import Morphology


class NoiseRemoval():

    def __init__(self):
        self.load_mask()
        self.morphology = Morphology()

    def load_mask(self, mask=None):
        self.mask = [[1, 1, 1],
                     [1, 1, 1],
                     [1, 1, 1]]

        self.mask = [[1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1]]

        # self.mask = [[1, 2, 1],
        #              [2, 4, 2],
        #              [1, 2, 1]]

        self.mask = [[1, 1, 2, 1, 1],
                     [1, 2, 4, 2, 1],
                     [2, 4, 8, 4, 2],
                     [1, 2, 4, 2, 1],
                     [1, 1, 2, 1, 1]]

        self.mask = mask or self.mask
        self.sum_mask = sum([sum(i) for i in self.mask])

    def median(self, pix, median=True):
        '''
        Median method
        '''
        pix_removal = [pix[i][:] for i in range(len(pix))]

        for i in range(len(self.mask)/2, len(pix) - len(self.mask)/2):
            for j in range(len(self.mask)/2, len(pix[0]) - len(self.mask)/2):
                for mi in range(len(self.mask)):
                    for mj in range(len(self.mask)):
                        pix_removal[i][j] += self.mask[mi][mj] * pix[i + mi - len(self.mask)/2][j + mj - len(self.mask)/2]

                pix_removal[i][j] /= self.sum_mask
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

    def opening(self, pix):
        pix = helper.gray_to_bin(pix)
        pix = self.morphology.opening(pix)
        pix = helper.binary_to_gray(pix)

        return pix


if __name__ == '__main__':
    noise_removal = NoiseRemoval()
    pix = [[100, 100, 100, 100, 100,],
           [100, 200, 205, 203, 100,],
           [100, 195, 200, 200, 100,],
           [100, 200, 205, 195, 100,],
           [100, 100, 100, 100, 100,]]
    print noise_removal.median(pix)