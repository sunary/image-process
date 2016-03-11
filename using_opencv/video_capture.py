__author__ = 'sunary'


import cv2
import numpy as np


def color_detect():
    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # lower_blue = np.array([110, 100, 100], dtype=np.uint8)
        # upper_blue = np.array([130, 255, 255], dtype=np.uint8)
        # mask = cv2.inRange(hsv, lower_blue, upper_blue)

        lower_white = np.array([0, 0, 100], dtype=np.uint8)
        upper_white = np.array([255, 70, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_white, upper_white)

        # res = cv2.bitwise_and(frame,frame, mask=mask)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        # cv2.imshow('res', res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    color_detect()