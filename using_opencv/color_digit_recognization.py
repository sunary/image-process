__author__ = 'sunary'


import cv2
import numpy as np


def add_edge(img, black=True):
    height, width = img.shape[:2]
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    if not black:
        img_gray = inverte(img_gray.copy())

    img_edge = auto_canny(img)
    for i in np.arange(height):
        for j in np.arange(width):
            if black:
                if img_edge[i][j] == 255:
                    img_gray[i][j] = 0
            else:
                if img_edge[i][j] == 255:
                    img_gray[i][j] = 255

    return img_gray


def auto_canny(img, sigma=0.33):
    v = np.median(img)

    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(img, lower, upper)

    return edged


def color_detect(img):
    lower = np.array((175, 175, 175), dtype=np.uint8)
    upper = np.array((255, 255, 255), dtype=np.uint8)

    if len(img.shape) == 3:
        mask = cv2.inRange(img, lower, upper)
    else:
        mask = cv2.inRange(img, np.mean(lower), np.mean(upper))

    # output = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow("color detection", np.hstack([img, mask]))
    return mask


def get_plate_flood(img_color, img):
    height, width = img.shape[:2]
    ratio = [0.9, 1.6]
    range_rect_width = (30, 120)
    check_point = []

    img_copy = img.copy()
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
                    if new_i > 0 and new_i < height - 1 and new_j > 0 and new_j < width - 1 and \
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
                    width_rect*1.0/height_rect > ratio[0] and width_rect*1.0/height_rect < ratio[1] and\
                    is_plate(img_color[min_y:max_y + 1, min_x:max_x + 1]):
                # cv2.rectangle(img_copy, (min_x, min_y), (max_x, max_y), (255), 2)
                rects.append((min_y, min_x, max_y + 1, max_x + 1))

            for i, j in relate_point:
                img[i][j] = 0

    return rects


def is_plate(img_plate):
    height, width = img_plate.shape[:2]

    boundaries = [((175, 175, 175), (255, 255, 255)), ((0, 0, 0), (80, 80, 80))]
    percent_color = []
    haft_percent_color = []

    for lower, upper in boundaries:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        img_plate_color = np.full((height, width), 0, dtype=np.uint8)

        for i in np.arange(height):
            for j in np.arange(width):
                # img_plate_color[i][j] = np.all(img_plate[i][j] > lower) and np.all(img_plate[i][j] < upper)
                img_plate_color[i][j] = np.mean(img_plate[i][j]) > np.mean(lower) and np.mean(img_plate[i][j]) < np.mean(upper)

        percent_color.append(np.sum(img_plate_color)*1.0/(height * width))
        haft_percent_color.append(np.sum(img_plate_color[height/4:height*3/4, width/4:width*3/4])*1.0/(height * width/4))

    print haft_percent_color
    return percent_color[1] > 0.04 and percent_color[0] > percent_color[1] + 0.15 and\
            percent_color[0] + percent_color[1] > 0.5


def remove_border(img):
    height, width = img.shape[:2]

    # img = np.vstack((np.full((1, width), 0, dtype=np.uint8), img, np.full((1, width), 0, dtype=np.uint8)))
    # height += 2
    # img = np.column_stack((np.full((height, 1), 0, dtype=np.uint8), img, np.full((height, 1), 0, dtype=np.uint8)))
    # width += 2

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

    return img


def inverte(img):
    return 255 - img


def digit_recongize(img):
    height, width = img.shape[:2]
    ratio = [0.15, 0.5]
    range_rect_height = (height*0.3, height*0.5)

    rects = []

    img_copy = img.copy()
    index = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(0, height):
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
                    rects.append((min_y, min_x, max_y + 1, max_x + 1))

    for rect in rects:
        cv2.imshow('digits %s' % (str(rect)), img[rect[0]:rect[2], rect[1]:rect[3]])

    # return img


if __name__ == '__main__':
    img_color = cv2.imread('/Users/sunary/Downloads/bs/xe2.jpg')
    img_gray = add_edge(img_color)

    img = color_detect(img_gray)
    cv2.imshow("rect detection", img)
    rects = get_plate_flood(img_color, img.copy())

    for r in rects:
        _img = remove_border(img[r[0]:r[2], r[1]:r[3]])
        digit_recongize(_img)
        # cv2.imshow("rect detection %s" %(str(r)), _img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()