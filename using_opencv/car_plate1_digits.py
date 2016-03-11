__author__ = 'sunary'


import cv2
import numpy as np
from using_opencv import xor_bit_image
import os
import scipy.misc
from using_opencv import deskew


def add_edge(img, color=False):
    height, width = img.shape[:2]

    mask_value = np.array([0, 0, 0]) if color else 0

    img_edge = auto_canny(img)
    for i in np.arange(height):
        for j in np.arange(width):
            if img_edge[i][j] == 255:
                img[i][j] = mask_value

    return img


def auto_canny(img, sigma=0.33):
    v = np.median(img)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)

    return edged


def color_detect(img, hsv=False):

    if hsv:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_white = np.array([0, 0, 120], dtype=np.uint8)
        upper_white = np.array([255, 70, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_white, upper_white)
    else:
        lower_white = np.array((175, 175, 175), dtype=np.uint8)
        upper_white = np.array((255, 255, 255), dtype=np.uint8)

        if len(img.shape) == 3:
            mask = cv2.inRange(img, lower_white, upper_white)
        else:
            mask = cv2.inRange(img, np.mean(lower_white), np.mean(upper_white))

    return mask


def get_plates_flood(img_color, img):
    height, width = img.shape[:2]
    ratio = [0.9, 1.6]
    range_rect_width = (100, 600)
    check_point = []

    rects = []

    for i in range(0, height - 1):
        for j in range(0, width - 1):
            if img[i][j] == 255:
                check_point.append((i, j))

    index = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for y, x in check_point:
        if img[y][x] == 255:
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
                            img[new_i][new_j] == 255 and (new_i, new_j) not in set_relate_point:
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

    return rects


def remove_border(img):
    img = deskew.deskew(img, is_binary=True)

    height, width = img.shape[:2]

    changed_point = []
    for j in range(width):
        if img[0][j] == 0:
            changed_point.append((0, j))
            img[0][j] = 255
        if img[height - 1][j] == 0:
            changed_point.append((height - 1, j))
            img[height - 1][j] = 255

    for i in range(1, height - 1):
        if img[i][0] == 0:
            changed_point.append((i, 0))
            img[i][0] = 255
        if img[i][width - 1] == 0:
            changed_point.append((i, width - 1))
            img[i][width - 1] = 255

    set_changed_point = set(changed_point)
    len_changed_point = len(changed_point)
    counter = 0
    index = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while counter < len_changed_point:
        y, x = changed_point[counter]
        for idx in index:
            if y + idx[0] >= 0 and y + idx[0] < height and x + idx[1] >= 0 and x + idx[1] < width and \
                    img[y + idx[0]][x + idx[1]] == 0 and (y + idx[0], x + idx[1]) not in set_changed_point:
                changed_point.append((y + idx[0], x + idx[1]))
                set_changed_point.add((y + idx[0], x + idx[1]))
                len_changed_point += 1
                img[y + idx[0]][x + idx[1]] = 255

        counter += 1

    range_number_color = (0.15, 0.40)

    img_area = width * height * 255
    sum_color = img_area - np.sum(img)

    if sum_color > range_number_color[0] * img_area and sum_color < range_number_color[1] * img_area:
        return img

    return None


def digit_recongize(img):
    height, width = img.shape[:2]
    ratio = [0.2, 0.55]
    range_rect_height = (height*0.25, height*0.45)

    rects = []
    img_numbers = []
    number_center_point = []

    img_copy = img.copy()
    index = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for j in range(width):
        for i in range(height):
            if img_copy[i][j] == 0:
                min_y = max_y = i
                min_x = max_x = j

                checked_point = [(i, j)]
                len_checked_point = len(checked_point)
                counter = 0
                while counter < len_checked_point:
                    y, x = checked_point[counter]

                    for idx in index:
                        if img_copy[y + idx[0]][x + idx[1]] == 0:
                            if y + idx[0] > max_y:
                                max_y = y + idx[0]
                            elif y + idx[0] < min_y:
                                min_y = y + idx[0]

                            if x + idx[1] > max_x:
                                max_x = x + idx[1]
                            elif x + idx[1] < min_x:
                                min_x = x + idx[1]

                            img_copy[y + idx[0]][x + idx[1]] = 255
                            checked_point.append((y + idx[0], x + idx[1]))
                            len_checked_point += 1

                    counter += 1

                width_rect = max_x - min_x
                height_rect = max_y - min_y

                if height_rect > range_rect_height[0] and height_rect < range_rect_height[1] and \
                        width_rect *1.0/height_rect > ratio[0] and width_rect *1.0/height_rect < ratio[1]:
                    rects.append((min_y, min_x, max_y + 1, max_x + 1))
                    img_numbers.append(img_from_black_point(checked_point, (height_rect + 1, width_rect + 1), (min_y, min_x)))
                    number_center_point.append(((min_y + max_y)/2, (min_x + max_x)/2))

    plate_nums = [[], []]
    for i, img_num in enumerate(img_numbers):
        # cv2.imshow('digits %s' % str(number_center_point[i]), img_num)
        num = get_number(img_num)
        if number_center_point[i][0] < height/2:
            plate_nums[0].append(num)
        else:
            plate_nums[1].append(num)

    return plate_nums[1]


def img_from_black_point(black_point, shape, start):
    new_img = np.full(shape, 255, dtype=np.uint8)
    for p in black_point:
        new_img[p[0] - start[0]][p[1] - start[1]] = 0

    return new_img


files_number = []
for i in range(10):
    files_number.append(os.path.dirname(__file__) + '/../resources/no_%s.jpg' % str(i))
xor_bit_image.load_image(files_number)

def get_number(img):
    return xor_bit_image.get_number(img)


def run(img_path):
    using_hsv = True

    img_color = cv2.imread(img_path)
    height, width = img_color.shape[:2]
    if width > 1000:
        img_color = scipy.misc.imresize(img_color, (height*1000/width, 1000))

    if using_hsv:
        img_color = add_edge(img_color, color=True)
        img = color_detect(img_color, hsv=True)
    else:
        img_gray = add_edge(img_color)
        img = color_detect(img_gray)

    # cv2.imshow("rect detection", img)
    rects = get_plates_flood(img_color, img.copy())

    for r in rects:
        _img = img[r[0]:r[2], r[1]:r[3]]
        # cv2.imshow("rect detection %s" %(str(r)), _img)
        _img = remove_border(_img)
        if _img is not None:
            # cv2.imshow("rect detection %s" %(str(r)), _img)
            print digit_recongize(_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run('/Users/sunary/Downloads/bs/bs_27889.jpg')