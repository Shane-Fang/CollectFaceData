import cv2
import os

'''
    控制OpenCV的類別，包括讀取鏡頭和儲存影像等等
'''

class CV:
    def __init__(self):
        self.cv = cv2
        self.camera = self.cv.VideoCapture(cv2.CAP_DSHOW)  # 設定影像來源為電腦鏡頭
        self.classfier = self.cv.CascadeClassifier("haarcascade_frontalface_default.xml")  # 載入辨識人臉工具
        self.frame = None  # 揁畫面
        self.color = (0, 255, 0)  # 邊框顏色
        self.person_name = ''  # 收集資料者的姓名
        self.num = 0  # count收集張數
        self.Collect = False  # 開啟收集功能
        self.dirPath = ''  # 存放影像路徑

    def read(self):  # 讀取鏡頭
        return self.camera.read()

    def getImg(self, frame):  # 獲取鏡頭影像轉成圖片，顯示在UI上或儲存成圖片檔
        self.frame = frame
        grey = self.cv.cvtColor(self.frame, self.cv.COLOR_BGR2GRAY)  # 影像RGB轉Gray
        faceRects = self.classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=5, minSize=(32, 32))  # 識別人臉

        if len(faceRects) > 0:  # 如果識別到人臉，則執行以下功能
            for faceRect in faceRects:
                x, y, w, h = faceRect  # 取得座標及長寬
                if self.Collect:  # 是否在收集資料
                    if os.path.isdir('%s/%s' % (self.dirPath, self.person_name)):  # 判斷是否有這路徑，沒有就創建
                        img_name = '%s/%s/%04d.jpg' % (self.dirPath, self.person_name, self.num)  # 圖片檔名
                        image = self.frame[y - 10: y + h + 10, x - 10: x + w + 10]  # 稍微放大一點
                        if image.size == 0:  # 如果上面的稍微放大一點的計算出現負數，圖片會沒有長寬，所以在這邊做個判斷
                            print('%s has problem' % self.num)
                        else:
                            self.num += 1  # 計數收集張數
                            self.cv.imwrite(img_name, image)  # 寫入圖檔
                        print(self.num)
                    else:
                        os.mkdir('%s/%s' % (self.dirPath, self.person_name))  # 創建路徑

                self.cv.rectangle(self.frame, (x - 10, y - 10), (x + w + 10, y + h + 10), self.color, 2)  # 畫框框

        return self.cv.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)  # 返回影像

    def CollectData(self, person_name: str):  # 收集圖片
        self.person_name = person_name
        self.Collect = True

    def close(self):  # 關閉影像串流

        self.camera.release()
        self.cv.destroyAllWindows()
