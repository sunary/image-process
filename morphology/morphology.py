__author__ = 'sunary'


from pprint import pprint
from utils import helper


class Morphology():

    def __init__(self):
        self.index = [[(-1, -1), (0, -1), (1, -1)],
                      [(-1, 0), (0, 0), (1, 0)],
                      [(-1, 1), (0, 1), (1, 1)]]
        self.pixel_bound = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]

    def dilation(self, pix):
        self.filter = [[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]]

        morphology_pix = [[0] * len(pix[0]) for _ in range(len(pix))]
        for i in range(1, len(pix) - 1):
            for j in range(1, len(pix[0]) - 1):
                if pix[i][j]:
                    for a in range(3):
                        for b in range(3):
                            if self.filter[a][b]:
                                morphology_pix[i + self.index[a][b][0]][j + self.index[a][b][1]] = 1

        return morphology_pix

    def erosion(self, pix):
        self.filter = [[-1, 1, -1],
                       [1, 1, 1],
                       [-1, 1, -1]]

        morphology_pix = [[0] * len(pix[0]) for _ in range(len(pix))]
        grid = [[0]* 3 for _ in range(3)]

        for i in range(1, len(pix) - 1):
            for j in range(1, len(pix[0]) - 1):
                if pix[i][j]:
                    for a in range(3):
                        for b in range(3):
                            grid[a][b] = pix[i + self.index[a][b][0]][j + self.index[a][b][1]]
                    if self.match_filter(self.filter, grid):
                        morphology_pix[i][j] = 1

        return morphology_pix

    def opening(self, pix):
        pix = self.erosion(pix)
        pix = self.dilation(pix)
        return pix

    def closing(self, pix):
        pix = self.dilation(pix)
        pix = self.erosion(pix)
        return pix

    def hit_and_mix(self, pix):
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

        morphology_pix = [[0] * len(pix[0]) for _ in range(len(pix))]
        grid = [[0] * 3 for _ in range(3)]

        for f in self.filter:
            for i in range(1, len(pix) - 1):
                for j in range(1, len(pix[0]) - 1):
                    if pix[i][j]:
                        for a in range(3):
                            for b in range(3):
                                grid[a][b] = pix[i + self.index[a][b][0]][j + self.index[a][b][1]]
                        if self.match_filter(f, grid):
                            morphology_pix[i][j] = 1

        return morphology_pix

    def thinning(self, pix):
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

        morphology_pix = pix
        grid = [[0]* 3 for _ in range(3)]

        have_change = True
        while have_change:
            have_change = False
            for f in self.filter:
                for i in range(1, len(pix) - 1):
                    for j in range(1, len(pix[0]) - 1):
                        if pix[i][j]:
                            for a in range(3):
                                for b in range(3):
                                    grid[a][b] = pix[i + self.index[a][b][0]][j + self.index[a][b][1]]
                            if self.match_filter(f, grid) and helper.count_connectivity(grid) == 1 and not self.end_point(grid):
                                morphology_pix[i][j] = 0
                                have_change = True
                pix = morphology_pix

        return morphology_pix

    def thickening(self, pix):
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

        grid = [[0] * 3 for _ in range(3)]

        have_change = True
        while have_change:
            have_change = False
            for f in self.filter:
                for i in range(1, len(pix) - 1):
                    for j in range(1, len(pix[0]) - 1):
                        if pix[i][j]:
                            for a in range(3):
                                for b in range(3):
                                    grid[a][b] = pix[i + self.index[a][b][0]][j + self.index[a][b][1]]
                            if self.match_filter(f, grid):
                                pix[i][j] = 0
                                have_change = True
        return pix

    def skeleton(self, pix):

        return pix

    def match_filter(self, filer, grid):
        for i in range(len(filer)):
            for j in range((len(filer[0]))):
                if filer[i][j] != -1 and filer[i][j] != grid[i][j]:
                    return False

        return True

    def end_point(self, grid):
        sum_point = 0
        for pos_bound in self.pixel_bound:
            sum_point += 1 if grid[pos_bound[0] + 1][pos_bound[1] + 1] else 0

        return sum_point <= 1


if __name__ == '__main__':
    morphology = Morphology()
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
    print '\ndilation'
    pprint(morphology.dilation(pix))

    print '\nerosion'
    pprint(morphology.erosion(pix))

    print '\nopening'
    pprint(morphology.opening(pix))

    print '\nclosing'
    pprint(morphology.closing(pix))

    print '\nthickening'
    pprint(morphology.thickening(pix))

    print '\nthinning'
    pprint(morphology.thinning(pix))

    print '\nhit_and_mix'
    pprint(morphology.hit_and_mix(pix))