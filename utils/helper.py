__author__ = 'sunary'


from PIL import Image


def gray_to_binary(pix):
    '''
    Examples:
        >>> gray_to_binary([[0xffffff, 0xffffff], [0, 0]])
        [[0, 0], [1, 1]]
    '''
    bin_pix = []

    for p in pix:
        bin_p = map(lambda x: 0 if x else 1, p)
        bin_pix.append(bin_p)

    return bin_pix


def binary_to_gray(pix):
    '''
    Examples:
        >>> binary_to_gray([[0, 0], [1, 1]])
        [[16777215, 16777215], [0, 0]]
    '''
    pix_gray = []

    for p in pix:
        gray_p = map(lambda x: 0x000000 if x else 0xffffff, p)
        pix_gray.append(gray_p)

    return pix_gray


def convert_gray(pix):
    pix_gray = [[0] * len(pix[0]) for _ in range(len(pix))]

    for i in range(len(pix)):
        for j in range(len(pix[0])):
            pix_gray[i][j] = (((pix[i][j] & 0x00ff0000) >> 16) + ((pix[i][j] & 0x0000ff00) >> 8) + (pix[i][j] & 0x000000ff))/3

    return pix_gray


def read_image(img_file):
    img = Image.open(img_file)
    data = img.getdata()

    pix = [[0] * img.size[1] for _ in range(img.size[0])]
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pix[i][j] = (data[j * img.size[0] + i][0] << 16) | (data[j * img.size[0] + i][1] << 8) | (data[j * img.size[0] + i][2])

    return pix


def save_image(pix, img_file, gray_image=False):
    with open(img_file, 'wb+'):
        pass

    img = Image.new(mode='RGB', size=(len(pix), len(pix[0])))

    if gray_image:
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                img.putpixel((i, j), (pix[i][j], pix[i][j], pix[i][j]))
    else:
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                img.putpixel((i, j), ((pix[i][j] & 0x00ff0000) >> 16, (pix[i][j] & 0x0000ff00) >> 8, (pix[i][j] & 0x000000ff)))

    img.save(img_file)


pixel_bound = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
def count_connectivity(grid):
    '''
    Examples:
        >>> count_connectivity([[1, 1, 0], [1, 1, 1], [1, 1, 0]])
        2
        >>> count_connectivity([[0, 1, 1], [1, 1, 1], [1, 1, 1]])
        1
    '''
    connectivity_number = 0
    need_new_connectivity = True

    for pos_bound in pixel_bound:
        if grid[pos_bound[0] + 1][pos_bound[1] + 1]:
            if need_new_connectivity:
                connectivity_number += 1
                need_new_connectivity = False
            if pos_bound == pixel_bound[-1] and grid[pixel_bound[-1][0] + 1][pixel_bound[-1][1] + 1]:
                connectivity_number = (connectivity_number - 1) if connectivity_number > 1 else connectivity_number
        else:
            need_new_connectivity = True

    return connectivity_number


if __name__ == '__main__':
    import doctest
    doctest.testmod()
