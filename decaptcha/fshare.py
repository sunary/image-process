__author__ = 'sunary'


import requests
import shutil
import cv2
import numpy as np
from preprocess import edge_detect
import matplotlib.pyplot as plt


def save_img(url_img):
    filename = ''
    res = requests.get(url_img, stream=True)
    if res.status_code == 200:
        with open(filename, 'wb') as of:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, of)

    return filename


def read_img(img_path):
    img = cv2.imread(img_path, cv2.THRESH_BINARY)

    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    img = remove_noise2(img)
    cv2.imshow('remove noise', img)


def remove_noise(img):
    kernel = np.ones((2, 2), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img

def remove_noise2(img):
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    _, img = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
    return img

def remove_noise3(img):
    return cv2.medianBlur(img, 5)

def remove_noise4(img):
    return cv2.fastNlMeansDenoising(img, None, 7, 7, 21)

def remove_noise5(img):
    return cv2.bilateralFilter(img, 9, 75, 75)


def flood_fill(img, value):
    img = np.copy(img)
    height, width = img.shape[:2]
    ratio = [0.25, 1.0]
    range_rect_width = (5, 20)
    check_point = []

    rects = []

    for i in range(0, height - 1):
        for j in range(0, width - 1):
            if img[i][j] == value:
                check_point.append((i, j))

    index = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for y, x in check_point:
        if img[y][x] == value:
            relate_point = [(y, x)]
            set_relate_point = set(relate_point)
            min_x = max_x = x
            min_y = max_y = y

            counter = 0
            len_relate_point = len(relate_point)
            while counter < len_relate_point:
                i = relate_point[counter][0]
                j = relate_point[counter][1]
                for idx in index:
                    new_i = i + idx[0]
                    new_j = j + idx[1]
                    if (new_i > 0 and new_i < height - 1) and (new_j > 0 and new_j < width - 1) and \
                            img[new_i][new_j] == value and (new_i, new_j) not in set_relate_point:
                        if new_i > max_y:
                            max_y = new_i
                        elif new_i < min_y:
                            min_y = new_i

                        if new_j > max_x:
                            max_x = new_j
                        elif new_j < min_x:
                            min_x = new_j

                        relate_point.append((new_i, new_j))
                        set_relate_point.add((new_i, new_j))
                        len_relate_point += 1

                counter += 1

            width_rect = max_x - min_x
            height_rect = max_y - min_y
            if width_rect > range_rect_width[0] and width_rect < range_rect_width[1] and \
                    width_rect *1.0/height_rect > ratio[0] and width_rect *1.0/height_rect < ratio[1]:
                rects.append((min_y, min_x, max_y + 1, max_x + 1))

            for i, j in relate_point:
                img[i][j] = 0

    # print len(rects)
    # print rects
    return rects


def get_numbers(img):
    pass


if __name__ == '__main__':
    read_img('/Users/sunary/Downloads/captcha_fshare.png')
    cv2.waitKey(0)
    cv2.destroyAllWindows()