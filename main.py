from tkinter import *
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk
from CV import CV
from sys import exit


def Descirption():  # 顯示使用說明視窗
    t = Tk()
    t.title("收集圖片")
    t.geometry('600x400')
    t.resizable(width=0, height=0)
    descirption = Label(t, text="\n\n1. 確認鏡頭是否開啟\n2. 在文字框輸入英文名字\n3. 選擇圖片儲存路徑\n4. 按下開始\n5. 在鏡頭面前晃晃你的頭"
                                "\n6. 等待資料收集完畢\n7. 把存圖片的資料夾壓縮傳給至\n\\\\192.168.5.5\Public\RD_11\劭勳\data", font='標楷體 20')
    descirption.pack()
    descirption.mainloop()


def check_contain_chinese(check_str):  # 檢查名字或路徑是否有中文或空格，返回Boolean
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            print(ch)
            return True

    if ' ' in check_str:
        return True

    return False


def Warning(txt: str):  # 顯示警告視窗
    messagebox.showinfo('警告', txt)


def start():  # 點擊開始按鈕事件
    if not name.get() or len(name.get()) == 0:  # 檢查名字輸入框是否為空
        Warning('請輸入英文名字')
        text.set('請輸入英文名字')
        return

    if not cv.dirPath or len(cv.dirPath) == 0:  # 檢查路徑是否為空
        Warning('請選擇路徑')
        text.set('請選擇路徑')
        return

    if not name.get().isalpha():  # 檢查名字是否都是英文
        name.delete(0, END)  # 清空名字輸入格
        Warning('名字內不可有中文、符號或空格')
        text.set('名字內不可有中文、符號或空格')
        return

    if check_contain_chinese(name.get()):  # 檢查名字是否有中文或空格，返回Boolean
        name.delete(0, END)
        Warning('名字內不可有中文、符號或空格')
        text.set('名字內不可有中文、符號或空格')
        return

    if check_contain_chinese(cv.dirPath):  # 檢查路徑是否有中文或空格，返回Boolean
        print(cv.dirPath)
        cv.dirPath = ''
        Warning('路徑內不可有中文或空格')
        text.set('路徑內不可有中文或空格')
        return

    setPath['state'] = DISABLED  # 設定按鈕為不可使用
    start_btn['state'] = DISABLED
    name['state'] = DISABLED

    cv.CollectData(name.get())  # 如果名字和路徑正確，就開始收集資料


def end():  # 點擊結束按鈕事件
    exit()


def selectPath():  # 點擊選擇路徑按鈕事件
    path = filedialog.askdirectory()  # 路徑選擇瀏覽器
    if not path or len(path) == 0:  # 檢查路徑是否為空
        text.set('請選擇路徑')
    else:
        cv.dirPath = path
        text.set('以選擇路徑:%s' % path)


def video_loop():  # 顯示鏡頭畫面的功能
    success, img = cv.read()  # 讀取鏡頭影像
    if success:  # 如果成功讀取
        cv2.waitKey(10)
        cv2image = cv.getImg(img)  # 獲取影像圖片

        if cv.Collect:  # 如果正在收集資料，則顯示收集進度
            text.set('已收集:%s/1000張' % cv.num)

        if cv.num == 1000:  # 如果收集完1000張，則結束收集
            cv.num = 0
            cv.Collect = False
            cv.person_name = None

            text.set('收集完畢')

            t = Tk()
            t.title("你的帥氣或美麗臉龐收集完成")  # 跳出結束提醒視窗
            t.geometry('500x200')
            t.resizable(width=0, height=0)
            descirption = Label(t, text="\n\n請把儲存圖片的資料夾壓縮傳至\n\\\\192.168.5.5\Public\RD_11\劭勳\data",
                                font='新細明體 20')
            descirption.pack()
            descirption.mainloop()

        current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=current_image)  # 用ImageTK將圖片顯示在label物件上
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        window.after(10, video_loop)  # UI迴圈，每10毫秒執行video_loop


cv = CV()

window = Tk(className='人臉影像收集')  # 建立UI
window.title("收集圖片")  # title
window.geometry('900x550')  # 大小
window.resizable(width=0, height=0)  # 設定不能放大縮小

text = StringVar()  # Tkinter文字，可以放進各種能顯示文字的物件上
text.set('輸入你的英文名字和選擇圖片儲存路徑')  # 設定文字

descirption = Button(window, text="說明", command=Descirption)  # 說明按鈕
descirption['width'] = 20  # 設定長寬
descirption['height'] = 3
descirption.place(x=700, y=50)  # 設定位置座標，左上角為(0, 0)

panel = Label(window)  # label物件，顯示影像用
panel.place(x=0, y=50)  # 設定位置座標

name = Entry(window, width=15, bd=6, font='Arial 20')  # 文字輸入框
name.place(x=650, y=150)  # 設定位置座標

label = Label(window, font="標楷體 16", textvariable=text, anchor=NW, wraplength=900)  # label物件，顯示上方文字提示
label['width'] = 80  # 設定長寬
label['height'] = 2
label.place(x=0, y=0)  # 設定位置座標

setPath = Button(window, text="選擇路徑", command=selectPath)  # 選擇路徑按鈕，command為上方的selectPath()
setPath['width'] = 20  # 設定長寬
setPath['height'] = 3
setPath.place(x=700, y=275)  # 設定位置座標

start_btn = Button(window, text="開始", command=start)  # 開始按鈕
start_btn['width'] = 20  # 設定長寬
start_btn['height'] = 3
start_btn.place(x=700, y=350)  # 設定位置座標

end_btn = Button(window, text="結束", command=end)  # 結束按鈕
end_btn['width'] = 20  # 設定長寬
end_btn['height'] = 3
end_btn.place(x=700, y=425)  # 設定位置座標

video_loop()

window.mainloop()  # UI 線程
cv.close()  # 關閉影像串流

