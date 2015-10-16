__author__ = 'sunary'


import cv2


class FaceDetect():

    def __init__(self):
        pass

    def process(self, cascade, nested_cascade, cam=None, img=None):
        cascade = cv2.CascadeClassifier(cascade)
        nested = cv2.CascadeClassifier(nested_cascade)

        if cam:
            pass
        elif img:
            img = cv2.imread(img)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            rects = self.detect(gray, cascade)
            vis = img.copy()
            self.draw_rects(vis, rects, (0, 255, 0))
            if not nested.empty():
                for x1, y1, x2, y2 in rects:
                    roi = gray[y1:y2, x1:x2]
                    vis_roi = vis[y1:y2, x1:x2]
                    subrects = self.detect(roi.copy(), nested)
                    self.draw_rects(vis_roi, subrects, (255, 0, 0))

            cv2.imshow('facedetect', vis)

    def detect(self, img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        return rects

    def draw_rects(self, img, rects, color):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

    def close(self):
        cv2.destroyAllWindows()


if __name__ == '__main__':
    face_detect = FaceDetect()
    face_detect.process('/../resources/haarcascade_frontalface_alt.xml', '/../resources/haarcascade_eye.xml', img='/../resources/face02.jpg')