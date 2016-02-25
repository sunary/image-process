__author__ = 'sunary'


import cv2
import numpy as np


def run():
    cap = cv2.VideoCapture(0)

    while(1):
        _, frame = cap.read()

        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([110, 50, 50], dtype=np.uint8)
        upper_blue = np.array([255, 255, 255], dtype=np.uint8)

        mask = cv2.inRange(frame, lower_blue, upper_blue)
        res = cv2.bitwise_and(frame,frame, mask=mask)

        # cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        # cv2.imshow('res', res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()