__author__ = 'sunary'


from PIL import Image


def gray_to_binary(pix):
    '''
    Examples:
        >>> gray_to_bin([[0xffffff, 0xffffff], [0, 0]])
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


if __name__ == '__main__':
    import doctest
    doctest.testmod()
