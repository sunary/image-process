__author__ = 'sunary'


import cv2
import numpy as np
import matplotlib.pyplot as plt


def normal(img):
    return cv2.equalizeHist(img)


def clahe(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    return clahe.apply(img)


def binary(img):
    _, bin_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return bin_img


def adaptive_mean(img):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)


def adaptive_gauss(img):
    return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4)


def ostu_algorithm(img, blursize=3):
    blur = cv2.GaussianBlur(img, (blursize, blursize), 0)
    hist = cv2.calcHist([blur], [0], None, [256], [0, 256])
    hist_norm = hist.ravel()/hist.max()
    Q = hist_norm.cumsum()
    bins = np.arange(256)
    fn_min = np.inf
    thresh = -1
    for i in xrange(1, 256):
        p1, p2 = np.hsplit(hist_norm, [i]) # probabilities
        q1, q2 = Q[i], Q[255] - Q[i] # cum sum of classes
        b1, b2 = np.hsplit(bins, [i]) # weights

        if q1 == 0: continue
        if q2 == 0: continue
        m1, m2 = np.sum(p1 * b1)/q1, np.sum(p2 * b2)/q2
        v1, v2 = np.sum(((b1 - m1) **2)*p1)/q1, np.sum(((b2 - m2) **2) *p2)/q2
        fn = v1*q1 + v2*q2

        if fn < fn_min:
            fn_min = fn
            thresh = i
    ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return otsu


def preview_hist(img):
    list_img = [img, normal(img), clahe(img)]
    title_img = ['origin', 'normal', 'clahe']
    for i in range(len(list_img)):
        plt.subplot(2, 2, i + 1)
        plt.imshow(list_img[i], 'gray')
        plt.title(title_img[i])

    plt.show()


def preview_bin(img):
    list_img = [binary(img), adaptive_mean(img), adaptive_gauss(img), ostu_algorithm(img)]
    title_img = ['binary', 'adaptive mean', 'adaptive gauss', 'ostu algorithm']
    for i in range(len(list_img)):
        plt.subplot(2, 2, i + 1)
        plt.imshow(list_img[i], 'gray')
        plt.title(title_img[i])

    plt.show()


def preview_combine(img, hist_type=0):
    if hist_type == 0:
        img = normal(img)
    elif hist_type == 1:
        img = clahe(img)

    list_img = [binary(img), adaptive_mean(img), adaptive_gauss(img), ostu_algorithm(img)]
    title_img = ['binary', 'adaptive mean', 'adaptive gauss', 'ostu algorithm']
    for i in range(len(list_img)):
        plt.subplot(2, 2, i + 1)
        plt.imshow(list_img[i], 'gray')
        plt.title(title_img[i])

    plt.show()


if __name__ == '__main__':
    img = cv2.imread('/Users/sunary/Downloads/bs/new_03.jpg', cv2.THRESH_BINARY)
    preview_combine(img, 0)