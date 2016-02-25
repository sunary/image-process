__author__ = 'sunary'


import cv2
import os


class FaceDetect():

    def __init__(self):
        self.current_dir = os.path.dirname(__file__)

    def process(self, cascade, nested_cascade, img_file):
        cascade = cv2.CascadeClassifier(self.current_dir + cascade)
        nested = cv2.CascadeClassifier(self.current_dir + nested_cascade)

        gray = cv2.imread(self.current_dir + img_file, 0)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.equalizeHist(gray)

        face_rects = self.detect(gray, cascade)
        vis = gray.copy()
        self.draw_rects(vis, face_rects, (0, 255, 0))
        if not nested.empty():
            for x1, y1, x2, y2 in face_rects:
                face_roi = gray[y1:y2, x1:x2]
                face_vis = vis[y1:y2, x1:x2]
                eyes_rects = self.detect(face_roi.copy(), nested)
                self.draw_rects(face_vis, eyes_rects, (255, 0, 0))

                # for x1, y1, x2, y2 in eyes_rects:
                #     eyes_roi = face_roi[y1:y2, x1:x2]
                #     eyes_vis = face_vis[y1:y2, x1:x2]
                #     circles = cv2.HoughCircles(eyes_roi, cv2.cv.CV_HOUGH_GRADIENT, 1 , 20, param1=50, param2=30, minRadius=0, maxRadius=0)
                #
                #     circles = np.uint16(np.around(circles))
                #     for i in circles[0, :]:
                #         cv2.circle(eyes_vis, (i[0], i[1]), i[2], (0, 255, 0), 2)

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
    face_detect = FaceDetect()
    face_detect.process('/../resources/haarcascade_frontalface_alt.xml',
                        '/../resources/haarcascade_eye.xml',
                        img_file='/../resources/face02.jpg')
    cv2.waitKey(0)
    cv2.destroyAllWindows()