__author__ = 'sunary'


import cv2
import numpy as np


def color_detect(img):
    boundaries = [((170, 170, 170), (255, 255, 255))]
    for lower, upper in boundaries:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(img, np.mean(lower), np.mean(upper))
        # output = cv2.bitwise_and(img, img, mask=mask)

        # cv2.imshow("color detection", np.hstack([img, mask]))
        return mask


def get_plate(img):
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

                        # cv2.line(img, (y, x), (y, x + width_rect), (255), 2)
                        # cv2.line(img, (y, x + width_rect), (y + height_rect, x + width_rect), (255), 2)
                        # cv2.line(img, (y, x), (y + height_rect, x), (255), 2)
                        # cv2.line(img, (y, x + width_rect), (y + height_rect, x + width_rect, ), (255), 2)

                        return img[y:y + height_rect, x:x + width_rect]

    print 'no'

def get_plate_flood(img):
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
            if width_rect and height_rect:
                print width_rect, height_rect, width_rect*1.0/height_rect
            if width_rect > range_rect_width[0] and width_rect < range_rect_width[1] and \
                width_rect*1.0/height_rect > ratio[0] and width_rect*1.0/height_rect < ratio[1]:
                return img[min_y:max_y, min_x:max_x]
            else:
                for i, j in relate_point:
                    img[i][j] = 0

def number():
    pass


if __name__ == '__main__':
    img = cv2.imread('/Users/sunary/Downloads/bs/bs_6789.jpg', cv2.THRESH_BINARY)
    height, width = img.shape[:2]
    print width, height
    # img = img[height/4:-height/4, width/4:-width/4]
    img = color_detect(img)
    cv2.imshow("color detection", img)
    img = get_plate_flood(img)
    if img is not None:
        cv2.imshow("rect detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()