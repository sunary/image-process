__author__ = 'sunary'


import cv2
import numpy as np
import bottleneck as bn
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pre_process.line_detect import LineDetect
from pre_process.edge_detect import EdgeDetect
from pre_process import histogram_equalization


def compute_skew(image):
    image = histogram_equalization.ostu_algorithm(image)

    edge = EdgeDetect()
    image = edge.process(image)
    # cv2.imshow('edge detect', image)

    line = LineDetect()
    return 180 - line.process(image, binary_image=True)[1]


def deskew(image, angle):
    image_center = (np.size(image, 1)/2, np.size(image, 0)/2)

    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
    result = cv2.warpAffine(image, rot_mat, (np.size(image, 1), np.size(image, 0)), flags=cv2.INTER_LINEAR)

    return result


def detect_line1(img):
    img = histogram_equalization.ostu_algorithm(img)

    edge = EdgeDetect()
    img = edge.process(img)
    # cv2.imshow('edge detect', img)

    lines = cv2.HoughLinesP(img, 1, np.pi/2, 2, minLineLength=200, maxLineGap=10)

    if lines is not None:
        for x1, y1, x2, y2 in lines[0]:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)

    return img


def detect_line2(img):
    img = histogram_equalization.ostu_algorithm(img)

    edge = EdgeDetect()
    img = edge.process(img)
    cv2.imshow('edge detect', img)

    sum_x = np.sum(img, axis=0)
    # max_xs = bn.argpartsort(-sum_x, 10)[:10]
    max_xs = sum_x.argsort()[-10:]

    sum_y = np.sum(img, axis=1)
    max_ys = bn.argpartsort(-sum_y, 10)[:10]

    height, width = img.shape[:2]

    for x in max_xs:
        cv2.line(img, (x, 0), (x, height), (255, 255, 255), 3)

    for y in max_ys:
        cv2.line(img, (0, y), (width, y), (255, 255, 255), 3)

    return img


def dectect_black_rect(img):
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
                if (array_equal(img[y + height_rect - 1:y + height_rect + 2, x - 1:x + 2], corner2)):
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
        cv2.imshow("color detection", np.hstack([img, mask]))


def compare_hist_equalization(img):
    plt.subplot(2, 2, 1)
    plt.imshow(histogram_equalization.normal(img), cmap=cm.Greys_r)
    plt.title('normal')

    plt.subplot(2, 2, 2)
    plt.imshow(histogram_equalization.clahe(img), cmap=cm.Greys_r)
    plt.title('clahe')

    plt.subplot(2, 2, 3)
    plt.imshow(histogram_equalization.adaptive(img), cmap=cm.Greys_r)
    plt.title('adaptive')

    plt.subplot(2, 2, 4)
    plt.imshow(histogram_equalization.ostu_algorithm(img), cmap=cm.Greys_r)
    plt.title('ostu')

    plt.show()


def recognize(img):
    angle = compute_skew(img)
    deskewed_image = deskew(img, angle)

    return deskewed_image
    rect_image = detect_line2(deskewed_image)

    cv2.imshow("lines detection", np.hstack([img, rect_image]))


if __name__ == '__main__':
    # img = cv2.imread('/Users/sunary/Downloads/TB015-1-10-2015/PA02TB0015598001-KT.jpg')
    img = cv2.imread('/Users/sunary/Downloads/TB015-1-10-2015/PA02TB0015598001-KT.jpg', cv2.THRESH_BINARY)
    height, width = img.shape[:2]
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = img[:-height/3, width/6:-width/6]
    print img.shape
    img = recognize(img)
    img = color_detection(img)

    black_rect = dectect_black_rect(img)
    cv2.imshow("lines detection", np.hstack([img, black_rect]))
    cv2.waitKey(0)
    cv2.destroyAllWindows()