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


def color_detection(img):
    boundaries = [((130, 130, 130), (255, 255, 255))]
    for lower, upper in boundaries:
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(img, np.mean(lower), np.mean(upper))
        output = cv2.bitwise_and(img, img, mask = mask)

        cv2.imshow("color detection", np.hstack([img, output]))


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
    height, width = img.shape[:2]

    angle = compute_skew(img[height/6:-height/6, width/6:-width/6])
    deskewed_image = deskew(img, angle)

    rect_image = detect_line2(deskewed_image)

    cv2.imshow("lines detection", np.hstack([img, rect_image]))


if __name__ == '__main__':
    img = cv2.imread('/Users/sunary/Downloads/TB015-1-10-2015/PA02TB0015598001-KT.jpg', cv2.THRESH_BINARY)
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # recognize(img)
    color_detection(img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()