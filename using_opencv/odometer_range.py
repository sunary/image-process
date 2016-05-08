__author__ = 'sunary'


import cv2
from using_opencv import color_processor


def run(img_path):
    img = cv2.imread(img_path, cv2.THRESH_BINARY)
    height, width = img.shape[:2]
    if width > 1000:
        img = cv2.resize(img, (1000, height*1000/width))

    img = color_processor.auto_canny(img)
    img = 255 - img

    cv2.imshow("color selection", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run('/Users/sunary/Downloads/odometer.jpg')