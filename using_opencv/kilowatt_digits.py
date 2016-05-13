__author__ = 'sunary'


from os import listdir
from os.path import isfile, join
import bottleneck as bn
import cv2
import numpy as np
from preprocess import deskew, edge_detect, line_detect


def detect_line_hough(img):
    img_edge = edge_detect.full_detect(img, is_binary=False)
    lines = cv2.HoughLinesP(img_edge, 1, np.pi/2, 2, minLineLength=200, maxLineGap=10)

    if lines is not None:
        for x1, y1, x2, y2 in lines[0]:
            # print (x1, y1), (x2, y2)
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 1)

    return img


def detect_line(img):
    img_edge = edge_detect.full_detect(img, is_binary=False)

    sum_x = np.sum(img_edge, axis=0)
    # max_xs = bn.argpartsort(-sum_x, 10)[:10]
    max_xs = sum_x.argsort()[-10:]

    sum_y = np.sum(img_edge, axis=1)
    max_ys = bn.argpartsort(-sum_y, 10)[:10]

    height, width = img_edge.shape[:2]

    for x in max_xs:
        # print (x, 0), (x, height)
        cv2.line(img, (x, 0), (x, height), (255, 255, 255), 1)

    for y in max_ys:
        # print (0, y), (width, y)
        cv2.line(img, (0, y), (width, y), (255, 255, 255), 1)

    return img


def detect_black_rect(img):
    height, width = img.shape[:2]
    get_percent = 0.01*255
    min_width, min_height = 100, 40

    cumsum = np.cumsum(img).reshape(height, width)

    check_point = []
    for i in range(1, height - min_height - 2):
        for j in range(1, width/2):
            check_point.append((i, j))

    corner1 = [['x', 0, 0], ['x', 0, 0], [255, 255, 255]]
    corner2 = [[0, 0, 'x'], [0, 0, 'x'], [255, 255, 255]]
    corner3 = [[255, 255, 255], ['x', 0, 0], ['x', 0, 0]]
    for y, x in check_point:
        if array_equal(img[y - 1:y + 2, x - 1:x + 2], corner1):
            arr_height = np.arange(min_height, height - y - 1)[::-1]
            i = 0

            while i < len(arr_height):
                height_rect = arr_height[i]
                if array_equal(img[y + height_rect - 1:y + height_rect + 2, x - 1:x + 2], corner2):
                    arr_width = np.arange(min_width, width - x - 1)[::-1]
                    j = 0

                    while j < len(arr_width):
                        width_rect = arr_width[j]
                        if (array_equal(img[y - 1:y + 2, x + width_rect - 1: x + width_rect + 2], corner3)) and \
                                (cumsum[y + height_rect][x + width_rect] + cumsum[y][x] - cumsum[y][x + width_rect] - cumsum[y + height_rect][x] < get_percent*height_rect*width_rect):
                            print (y, x, y + height_rect, x + width_rect)

                            cv2.rectangle(img, (x, y), (x + width_rect, y + height_rect), (255), 2)

                            i = len(arr_height)
                            j = len(arr_width)
                        j += 1
                i += 1

    return img


def array_equal(arr1, arr2):
    for i in range(len(arr2)):
        for j in range(len(arr2[0])):
            if arr2[i][j] != 'x' and arr1[i][j] != arr2[i][j]:
                return False

    return True


def color_detection(img):
    boundaries = [((130, 130, 130), (255, 255, 255))]
    for lower, upper in boundaries:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(img, np.mean(lower), np.mean(upper))
        # output = cv2.bitwise_and(img, img, mask = mask)

        return mask


def make_deskew(img):
    height, width = img.shape[:2]

    angle = deskew.compute_skew(img[height/4:height*3/4, width/4:width*3/4], is_binary=False)
    deskewed_image = deskew.deskew(img, angle=angle, is_binary=False)

    return deskewed_image


def run(img_path):
    img = cv2.imread(img_path, cv2.THRESH_BINARY)
    height, width = img.shape[:2]
    if width > 1000:
        img = cv2.resize(img, (1000, height*1000/width))

    # img = color_processor.auto_canny(img)
    # cv2.imshow('color selection', img)

    img_deskew = make_deskew(img)
    # img_lines = detect_line_hough(img_deskew)
    # img_lines = line_detect.houghlines(img)
    img_boudingbox = edge_detect.bounding_box(img_deskew, range_w=[10, 30], range_h=[20, 60])[0]

    cv2.imshow('lines detection', np.hstack([img_deskew, img_boudingbox]))


def run_list(path):
    img_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    id = 17

    while True:
        run(img_files[id])
        pressed_key = cv2.waitKey()
        if pressed_key == ord('a'): # up
            id = (id - 1 + len(img_files)) %(len(img_files))
            continue
        elif pressed_key == ord('s'): # down
            id = (id + 1) %(len(img_files))
            continue
        else:
            break


if __name__ == '__main__':
    run_list('/Users/sunary/Downloads/vzota/TB015-1-10-2015')