__author__ = 'sunary'


from pprint import pprint
from PIL import Image


class Morphology():

    def __init__(self):
        self.index = [[(-1, -1), (0, -1), (1, -1)],
                      [(-1, 0), (0, 0), (1, 0)],
                      [(-1, 1), (0, 1), (1, 1)]]
        self.pixel_bound = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

        self.size_img = (0, 0)

    def read_image(self):
        self.img = Image.open(self.current_dir + '/../resources/face02.jpg')
        data = self.img.getdata()

        self.size_img = (self.img.size[0], self.img.size[1])
        self.pix = [[0]*self.size_img[1] for _ in range(self.size_img[0])]
        self.morphology_pix = [[0]*self.size_img[1] for _ in range(self.size_img[0])]
        for i in range(self.size_img[0]):
            for j in range(self.size_img[1]):
                self.pix[i][j] = (data[j*self.size_img[1] + i][0] << 16) | (data[j*self.size_img[1] + i][1] << 8) | (data[j*self.size_img[1] + i][2])

    def save_image(self):
        for i in range(self.size_img[0]):
            for j in range(self.size_img[1]):
                self.img.putpixel((i, j), ((self.pix[i][j] & 0x00ff0000) >> 16, (self.pix[i][j] & 0x0000ff00) >> 8, (self.pix[i][j] & 0x000000ff)))
        self.img.save(self.current_dir + '/../resources/result.png')

    def set_pix(self, pix):
        self.pix = pix
        self.size_img = (len(self.pix), len(self.pix[0]))

    def dilation(self):
        print 'dilation'
        self.filter = [[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]]

        self.morphology_pix = [[0]*self.size_img[1] for _ in range(self.size_img[0])]
        for i in range(1, self.size_img[0] - 1):
            for j in range(1, self.size_img[1] - 1):
                if self.pix[i][j]:
                    for a in range(3):
                        for b in range(3):
                            if self.filter[a][b]:
                                self.morphology_pix[i + self.index[a][b][0]][j + self.index[a][b][1]] = 1

    def erosion(self):
        print 'erosion'
        self.filter = [[-1, 1, -1],
                       [1, 1, 1],
                       [-1, 1, -1]]

        self.morphology_pix = [[0]*self.size_img[1] for _ in range(self.size_img[0])]
        grid = [[0]* 3 for i in range(3)]
        for i in range(1, self.size_img[0] - 1):
            for j in range(1, self.size_img[1] - 1):
                if self.pix[i][j]:
                    for a in range(3):
                        for b in range(3):
                            grid[a][b] = self.pix[i + self.index[a][b][0]][j + self.index[a][b][1]]
                    if self.match_filter(self.filter, grid):
                        self.morphology_pix[i][j] = 1

    def opening(self):
        print 'opening'
        self.erosion()
        self.dilation()

    def closing(self):
        print 'closing'
        self.dilation()
        self.erosion()

    def hit_and_mix(self):
        print 'hit_and_mix'
        self.filter = [[[-1, 1, -1],
                       [0, 1, 1],
                       [0, 0, -1]],
                        [[0, 0, -1],
                       [0, 1, 1],
                       [-1, 1, -1]],
                        [[-1, 0, 0],
                       [1, 1, 0],
                       [-1, 1, -1]],
                        [[-1, 1, -1],
                       [1, 1, 0],
                       [-1, 0, 0]]]

        self.morphology_pix = [[0]*self.size_img[1] for _ in range(self.size_img[0])]
        grid = [[0]* 3 for i in range(3)]
        for f in self.filter:
            for i in range(1, self.size_img[0] - 1):
                for j in range(1, self.size_img[1] - 1):
                    if self.pix[i][j]:
                        for a in range(3):
                            for b in range(3):
                                grid[a][b] = self.pix[i + self.index[a][b][0]][j + self.index[a][b][1]]
                        if self.match_filter(f, grid):
                            self.morphology_pix[i][j] = 1

    def thinning(self):
        print 'thinning'
        self.filter = [[[-1, -1, -1],
                       [1, 1, 0],
                       [-1, -1, -1]],
                        [[-1, 1, -1],
                       [-1, 1, 1],
                       [-1, 0, -1]],
                        [[-1, -1, -1],
                       [0, 1, 1],
                       [-1, -1, -1]],
                        [[-1, 0, -1],
                       [-1, 1, -1],
                       [-1, 1, -1]]]

        self.morphology_pix = self.pix
        grid = [[0]* 3 for i in range(3)]
        have_change = True
        while have_change:
            have_change = False
            for f in self.filter:
                for i in range(1, self.size_img[0] - 1):
                    for j in range(1, self.size_img[1] - 1):
                        if self.pix[i][j]:
                            for a in range(3):
                                for b in range(3):
                                    grid[a][b] = self.pix[i + self.index[a][b][0]][j + self.index[a][b][1]]
                            if self.match_filter(f, grid) and self.count_connectivity(grid) == 1 and not self.end_point(grid):
                                self.morphology_pix[i][j] = 0
                                have_change = True
                self.pix = self.morphology_pix

    def thickening(self):
        print 'thickening'
        self.filter = [[[-1, 1, -1],
                       [0, 1, 1],
                       [0, 0, -1]],
                        [[0, 0, -1],
                       [0, 1, 1],
                       [-1, 1, -1]],
                        [[-1, 0, 0],
                       [1, 1, 0],
                       [-1, 1, -1]],
                        [[-1, 1, -1],
                       [1, 1, 0],
                       [-1, 0, 0]],
                        [[1, 1, 1],
                       [-1, 1, -1],
                       [0, 0, 0]],
                        [[0, -1, 1],
                       [0, 1, 1],
                       [0, -1, 1]],
                        [[0, 0, 0],
                       [-1, 1, -1],
                       [1, 1, 1]],
                        [[1, -1, 0],
                       [1, 1, 0],
                       [1, -1, 0]]]

        grid = [[0]* 3 for i in range(3)]
        have_change = True
        while have_change:
            have_change = False
            for f in self.filter:
                for i in range(1, self.size_img[0] - 1):
                    for j in range(1, self.size_img[1] - 1):
                        if self.pix[i][j]:
                            for a in range(3):
                                for b in range(3):
                                    grid[a][b] = self.pix[i + self.index[a][b][0]][j + self.index[a][b][1]]
                            if self.match_filter(f, grid):
                                self.pix[i][j] = 0
                                have_change = True
        self.morphology_pix = self.pix

    def skeleton(self):
        print 'skeleton'

    def count_connectivity(self, grid):
        connectivity_number = 0
        need_new_connectivity = True

        for posbound in self.pixel_bound:
            if grid[posbound[0] + 1][posbound[1] + 1]:
                if need_new_connectivity:
                    connectivity_number += 1
                    need_new_connectivity = False
                if posbound == self.pixel_bound[-1] and grid[self.pixel_bound[-1][0] + 1][self.pixel_bound[-1][1] + 1]:
                    connectivity_number = (connectivity_number - 1) if connectivity_number > 1 else connectivity_number
            else:
                need_new_connectivity = True

        return connectivity_number

    def match_filter(self, filer, grid):
        for i in range(len(filer)):
            for j in range((len(filer[0]))):
                if filer[i][j] != -1 and filer[i][j] != grid[i][j]:
                    return False

        return True

    def end_point(self, grid):
        sum_point = 0
        for posbound in self.pixel_bound:
            sum_point += grid[posbound[0] + 1][posbound[1] + 1]

        return sum_point <= 1


if __name__ == '__main__':
    morphology = Morphology()
    morphology.set_pix(pix= [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0],
                      [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
                      [0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                      [0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]])
    #
    # morphology.erosion()
    # pprint(morphology.morphology_pix)
    #
    # morphology.pix = morphology.morphology_pix
    # morphology.dilation()
    # pprint(morphology.morphology_pix)
    #
    # morphology.pix = morphology.morphology_pix
    # morphology.thinning()
    # pprint(morphology.morphology_pix)
    #
    # morphology.pix = morphology.morphology_pix
    morphology.thinning()
    pprint(morphology.morphology_pix)
