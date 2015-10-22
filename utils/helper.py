__author__ = 'sunary'


from PIL import Image


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

def save_image(pix, img_file):
    with open(img_file, 'wb+'):
        pass

    img = Image.new(mode='RGB', size=(len(pix), len(pix[0])))

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            img.putpixel((i, j), ((pix[i][j] & 0x00ff0000) >> 16, (pix[i][j] & 0x0000ff00) >> 8, (pix[i][j] & 0x000000ff)))

    img.save(img_file)
