__author__ = 'sunary'


import cv2
import numpy as np


def color_detect(img):
    lower = np.array((175, 175, 175), dtype=np.uint8)
    upper = np.array((255, 255, 255), dtype=np.uint8)

    mask = cv2.inRange(img, np.mean(lower), np.mean(upper))
    # output = cv2.bitwise_and(img, img, mask=mask)

    # cv2.imshow("color detection", np.hstack([img, mask]))
    return mask


def get_plate(img):
    height, width = img.shape[:2]
    ratio = [1.3, 1.5]
    range_rect_width = (180, 300)
    corner = np.array([[255, 255, 255], [255, 255, 255], [255, 255, 255]])

    check_point = []
    for i in range(height/4, height/2):
        for j in range(width/4, width/2):
            check_point.append((i, j))

    for x, y in check_point:
        if np.array_equal(img[y - 1:y + 2, x - 1: x + 2], corner):
            arr_height = np.arange(int(range_rect_width[0]/ratio[0]), min(int(range_rect_width[1]/ratio[1]), height - y - 1))[::-1]
            arr_width = np.arange(range_rect_width[0], min(range_rect_width[1], width - x - 1))[::-1]

            for height_rect in arr_height:
                for width_rect in arr_width:
                    if np.array_equal(img[y - 1:y + 2, x + width_rect - 1: x + width_rect + 2], corner) and \
                            np.array_equal(img[y + height_rect - 1:y + height_rect + 2, x - 1: x + 2], corner) and \
                            np.array_equal(img[y+ height_rect - 1:y + height_rect + 2, x + width_rect- 1: x + width_rect + 2], corner) and \
                            width_rect*1.0/height_rect > ratio[0] and width_rect*1.0/height_rect < ratio[1]:
                        print (y, x, y + height_rect, x + width_rect)
                        cv2.rectangle(img, (x, y), (x + width_rect, y + height_rect), (255), 2)

                        return img[y:y + height_rect, x:x + width_rect]

    print 'no'


def get_plate_flood(img):
    height, width = img.shape[:2]
    ratio = [1.27, 1.5]
    range_rect_width = (150, 350)
    check_point = []

    for i in range(height/4, height/2):
        for j in range(width/4, width/2):
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
                    if new_i > height/4 and new_i < height*3/4 and new_j > width/4 and new_j < width*3/4 and \
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
                    width_rect*1.0/height_rect > ratio[0] and width_rect*1.0/height_rect < ratio[1]:
                return img[min_y:max_y, min_x:max_x]
            else:
                for i, j in relate_point:
                    img[i][j] = 0


def remove_border(img):
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
            if y + idx[0] >= 0 and y + idx[0] < height - 1 and x + idx[1] >= 0 and x + idx[1] < width - 1 and \
                    img[y + idx[0]][x + idx[1]] == 0 and (y + idx[0], x + idx[1]) not in set_changed_point:
                changed_point.append((y + idx[0], x + idx[1]))
                set_changed_point.add((y + idx[0], x + idx[1]))
                len_changed_point += 1
                img[y + idx[0]][x + idx[1]] = 255

        counter += 1

    return img

def inverte(img):
    return 255 - img


def digit_recongize(img):
    height, width = img.shape[:2]
    ratio = [0.22, 0.5]
    range_rect_height = (height*0.39, height*0.46)

    rects = []

    img_copy = img.copy()
    index = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(height/2, height):
        for j in range(width):
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
                        width_rect*1.0/height_rect > ratio[0] and width_rect*1.0/height_rect < ratio[1]:
                    rects.append((min_y, min_x, height_rect, width_rect))

    for rect in rects:
        cv2.imshow('digits %s' % (str(rect)), img[rect[0]:rect[0] + rect[2], rect[1]:rect[1] + rect[3]])

    return img


def run(img_path):
    img = cv2.imread(img_path, cv2.THRESH_BINARY)
    img = color_detect(img)
    # cv2.imshow("color detection", img)
    img = get_plate_flood(img)
    if img is not None:
        img = remove_border(img)
        digit_recongize(img)
        # cv2.imshow("rect detection", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run('/Users/sunary/Downloads/bs/bs_6789.jpg')