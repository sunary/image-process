__author__ = 'sunary'


from PIL import Image
import os


class LineDetect():

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


if __name__ == '__main__':
    line_detect = LineDetect()
    line_detect.read_image()