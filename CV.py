import cv2
import os


class CV:
    def __init__(self):
        self.cv = cv2
        self.camera = self.cv.VideoCapture(cv2.CAP_DSHOW)
        self.classfier = self.cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.frame = None
        self.color = (0, 255, 0)
        self.person_name = ''
        self.num = 0
        self.Collect = False
        self.dirPath = ''

    def read(self):
        return self.camera.read()

    def getImg(self, frame):
        self.frame = frame
        grey = self.cv.cvtColor(self.frame, self.cv.COLOR_BGR2GRAY)
        faceRects = self.classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=5, minSize=(32, 32))

        if len(faceRects) > 0:
            for faceRect in faceRects:
                x, y, w, h = faceRect
                if self.Collect:
                    if os.path.isdir('%s/%s' % (self.dirPath, self.person_name)):
                        img_name = '%s/%s/%04d.jpg' % (self.dirPath, self.person_name, self.num)
                        image = self.frame[y - 10: y + h + 10, x - 10: x + w + 10]
                        if image.size == 0:
                            print('%s have problem' % self.num)
                        else:
                            self.num += 1
                            self.cv.imwrite(img_name, image)
                        print(self.num)
                    else:
                        os.mkdir('%s/%s' % (self.dirPath, self.person_name))

                self.cv.rectangle(self.frame, (x - 10, y - 10), (x + w + 10, y + h + 10), self.color, 2)

        return self.cv.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)

    def CollectData(self, person_name: str):
        self.person_name = person_name
        self.Collect = True

    def close(self):
        self.camera.release()
        self.cv.destroyAllWindows()
