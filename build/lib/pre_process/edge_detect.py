__author__ = 'sunary'


from utils import helper
import os


class EdgeDetect():

    def __init__(self):
        pass

    def process(self, pix):
        temp_x = [[0] * len(pix[0]) for _ in range(len(pix))]
        temp_y = [[0] * len(pix[0]) for _ in range(len(pix))]

        edge_pix = [[0] * len(pix[0]) for _ in range(len(pix))]

        self._sobel()

        for i in range(len(self.gx)/2, len(pix) - len(self.gx)/2):
            for j in range(len(self.gx)/2, len(pix[0]) - len(self.gy)/2):
                for d1 in range(len(self.gx)):
                    for d2 in range(len(self.gx)):
                        temp_x[i][j] += self.gx[d1][d2] * pix[i + d1 - 1][j + d2 -1]
                        temp_y[i][j] += self.gy[d1][d2] * pix[i + d1 - 1][j + d2 -1]

        for i in range(0, len(pix) - 0):
            for j in range(0, len(pix[0]) - 0):
                edge_pix[i][j] = 0x000000 if (temp_x[i][j]*temp_x[i][j] + temp_y[i][j]*temp_y[i][i] > self.threshold) else 0xffffff

        return edge_pix

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
                   [1, 2, 0, -2, 1]]
        self.gy = [[-1, -4, -6, -4, -1],
                   [-2, -8, -12, -8, -2],
                   [0, 0, 0, 0, 0],
                   [2, 8, 12, 8, 2],
                   [1, 4, 6, 4, 1]]

        self.threshold = 4000

    def _robert(self):
        self.gx = [[1, 0],
                [0, -1]]
        self.gy = [[0, 1],
                [-1, 0]]

        self.threshold = 400

    def _prewitt(self):
        self.gx = [[-1, 0, 1],
                  [-1, 0, 1],
                  [-1, 0, 1]]
        self.gy = [[-1, -1, -1],
                  [0, 0, 0],
                  [1, 1, 1]]

        self.threshold = 2000


if __name__ == '__main__':
    edge_detect = EdgeDetect()
    pix = helper.read_image(os.path.dirname(__file__) + '/../resources/face02.jpg')
    pix = helper.convert_gray(pix)
    pix = edge_detect.process(pix)
    helper.save_image(os.path.dirname(__file__) + '/../resources/result.png')