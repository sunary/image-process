__author__ = 'sunary'


from utils import helper
import os
import cv2
import numpy as np
from preprocess import edge_detect
from preprocess.noise_removal import NoiseRemoval
from morphology.morphology import Morphology


class IrisDetect():

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)
        self.noise_removal = NoiseRemoval()
        self.morphology = Morphology()

    def process(self, cascade, nested_cascade, img_file):
        cascade = cv2.CascadeClassifier(self.current_dir + cascade)
        nested = cv2.CascadeClassifier(self.current_dir + nested_cascade)

        gray = cv2.imread(self.current_dir + img_file, 0)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.equalizeHist(gray)

        face_rects = self.detect(gray, cascade)
        vis = gray.copy()
        self.draw_rects(vis, face_rects, (0, 255, 0))

        eye_count = 0
        if not nested.empty():
            for x1, y1, x2, y2 in face_rects:
                face_roi = gray[y1:y2, x1:x2]
                face_vis = vis[y1:y2, x1:x2]

                eyes_rects = self.detect(face_roi.copy(), nested)
                self.draw_rects(face_vis, eyes_rects, (255, 0, 0))

                for x1, y1, x2, y2 in eyes_rects:
                    eyes_roi = face_roi[y1:y2, x1:x2]

                    edge_eyes_roi = edge_detect.edge_detect(eyes_roi)
                    helper.save_image(edge_eyes_roi, self.current_dir + '/../resources/eyes_roi%s.png' %(eye_count))

                    # edge_eyes_roi = self.noise_removal.median(edge_eyes_roi)
                    edge_eyes_roi = self.noise_removal.opening(edge_eyes_roi)
                    helper.save_image(edge_eyes_roi, self.current_dir + '/../resources/eyes_roi_noise_removal%s.png' %(eye_count))
                    eye_count += 1

                    edge_eyes_roi = np.array(edge_eyes_roi, dtype=np.uint8)
                    eyes_vis = face_vis[y1:y2, x1:x2]

                    circles = cv2.HoughCircles(edge_eyes_roi, cv2.cv.CV_HOUGH_GRADIENT, 1 , 20, param1=50, param2=30, minRadius=0, maxRadius=0)
                    if circles is not None:
                        circles = np.uint16(np.around(circles))
                        for i in circles[0, :]:
                            cv2.circle(eyes_vis, (i[0], i[1]), i[2], (0, 255, 0), 2)

        cv2.imshow('face detect', vis)

    def detect(self, img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:, 2:] += rects[:, :2]
        return rects

    def draw_rects(self, img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


if __name__ == '__main__':
    iris_detect = IrisDetect()
    iris_detect.process('/../resources/haarcascade_frontalface_alt.xml',
                        '/../resources/haarcascade_eye.xml',
                        img_file='/../resources/me.jpg')
    cv2.waitKey(0)
    cv2.destroyAllWindows()