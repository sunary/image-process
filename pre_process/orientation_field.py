__author__ = 'sunary'

from PIL import Image
import math
import os


class OrientationField():

    SIZE_ORIENTATION = (10, 10)
    def __init__(self):
        self.current_dir = os.path.dirname(__file__)

    def read_image(self):
        self.img = Image.open(self.current_dir + '/../resources/face.jpg')
        data = self.img.getdata()

        self.pix = [[0]*self.img.size[1] for _ in range(self.img.size[0])]
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                self.pix[i][j] = (data[j*self.img.size[0] + i][0] << 16) | (data[j*self.img.size[0] + i][1] << 8) | (data[j*self.img.size[0] + i][2])

    def save_image(self):
        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                self.img.putpixel((i, j), ((self.pix[i][j] & 0x00ff0000) >> 16, (self.pix[i][j] & 0x0000ff00) >> 8, (self.pix[i][j] & 0x000000ff)))
        self.img.save(self.current_dir + '/../resources/result.png')

    def process(self):
        temp_x = [[0]*self.img.size[1] for _ in range(self.img.size[0])]
        temp_y = [[0]*self.img.size[1] for _ in range(self.img.size[0])]

        self._sobel()

        for i in range(1, self.img.size[0] - 1):
            for j in range(1, self.img.size[1] - 1):
                for d1 in range(len(self.gx)):
                    for d2 in range(len(self.gx)):
                        temp_x[i][j] += self.gx[d1][d2]*self.pix_gray[i + d1 - 1][j + d2 -1]
                        temp_y[i][j] += self.gy[d1][d2]*self.pix_gray[i + d1 - 1][j + d2 -1]

        orient = [[0]* self.SIZE_ORIENTATION[1]]* self.SIZE_ORIENTATION[0]
        coherence = [[0]* self.SIZE_ORIENTATION[1]]* self.SIZE_ORIENTATION[0]
        for m in range(self.SIZE_ORIENTATION[0]):
            for n in range(self.SIZE_ORIENTATION[1]):
                sum_j1 = 0.0
                sum_j2 = 0.0
                sum_j3 = 0.0
                for i in range(self.img.size[0]/self.SIZE_ORIENTATION[0]):
                    for j in range(self.img.size[1]/self.SIZE_ORIENTATION[1]):
                        sum_j1 += 2*temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]
                        sum_j2 += temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j] - temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]
                        sum_j3 += temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_x[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j] + temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]*temp_y[m*self.SIZE_ORIENTATION[0] + i][n*self.SIZE_ORIENTATION[1] + j]

                orient[m][n] = math.atan(sum_j1/sum_j2)/2
                coherence[m][n] = math.sqrt(sum_j1*sum_j1 + sum_j2*sum_j2)/sum_j3

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
