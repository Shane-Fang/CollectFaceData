from tkinter import *
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk
from CV import CV
from sys import exit


def Descirption():
    t = Tk()
    t.title("收集圖片")
    t.geometry('600x400')
    t.resizable(width=0, height=0)
    descirption = Label(t, text="\n\n1. 確認鏡頭是否開啟\n2. 在文字框輸入英文名字\n3. 選擇圖片儲存路徑\n4. 按下開始\n5. 在鏡頭面前晃晃你的頭"
                                "\n6. 等待資料收集完畢\n7. 把存圖片的資料夾壓縮傳給至\n\\\\192.168.5.5\Public\RD_11\劭勳\data", font='標楷體 20')
    descirption.pack()
    descirption.mainloop()


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            print(ch)
            return True

    if ' ' in check_str:
        return True

    return False


def Warning(txt: str):
    messagebox.showinfo('警告', txt)


def start():
    if not name.get() or len(name.get()) == 0:
        Warning('請輸入英文名字')
        text.set('請輸入英文名字')
        return

    if not cv.dirPath or len(cv.dirPath) == 0:
        Warning('請選擇路徑')
        text.set('請選擇路徑')
        return

    if not name.get().isalpha():
        name.delete(0, END)
        Warning('名字內不可有中文、符號或空格')
        text.set('名字內不可有中文、符號或空格')
        return

    if check_contain_chinese(name.get()):
        name.delete(0, END)
        Warning('名字內不可有中文、符號或空格')
        text.set('名字內不可有中文、符號或空格')
        return

    if check_contain_chinese(cv.dirPath):
        print(cv.dirPath)
        cv.dirPath = ''
        Warning('路徑內不可有中文或空格')
        text.set('路徑內不可有中文或空格')
        return

    setPath['state'] = DISABLED
    start_btn['state'] = DISABLED
    name['state'] = DISABLED

    cv.CollectData(name.get())


def end():
    exit()


def selectPath():
    path = filedialog.askdirectory()
    if not path or len(path) == 0:
        text.set('請選擇路徑')
    else:
        cv.dirPath = path
        text.set('以選擇路徑:%s' % path)


def video_loop():
    success, img = cv.read()
    if success:
        cv2.waitKey(10)
        cv2image = cv.getImg(img)

        if cv.Collect:
            text.set('已收集:%s/1000張' % cv.num)

        if cv.num == 1000:
            cv.num = 0
            cv.Collect = False
            cv.person_name = None

            text.set('收集完畢')

            t = Tk()
            t.title("你的帥氣或美麗臉龐收集完成")
            t.geometry('500x200')
            t.resizable(width=0, height=0)
            descirption = Label(t, text="\n\n請把儲存圖片的資料夾壓縮傳至\n\\\\192.168.5.5\Public\RD_11\劭勳\data",
                                font='新細明體 20')
            descirption.pack()
            descirption.mainloop()

        current_image = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        window.after(10, video_loop)


cv = CV()

window = Tk(className='人臉影像收集')
window.title("收集圖片")
window.geometry('900x550')
window.resizable(width=0, height=0)

text = StringVar()
text.set('輸入你的英文名字和選擇圖片儲存路徑')

descirption = Button(window, text="說明", command=Descirption)
descirption['width'] = 20
descirption['height'] = 3
descirption.place(x=700, y=50)

panel = Label(window)
panel.place(x=0, y=50)
window.config(cursor="arrow")

name = Entry(window, width=15, bd=6, font='Arial 20')
name.place(x=650, y=150)

label = Label(window, font="標楷體 16", textvariable=text, anchor=NW, wraplength=900)
label['width'] = 80
label['height'] = 2
label.place(x=0, y=0)

setPath = Button(window, text="選擇路徑", command=selectPath)
setPath['width'] = 20
setPath['height'] = 3
setPath.place(x=700, y=275)

start_btn = Button(window, text="開始", command=start)
start_btn['width'] = 20
start_btn['height'] = 3
start_btn.place(x=700, y=350)

end_btn = Button(window, text="結束", command=end)
end_btn['width'] = 20
end_btn['height'] = 3
end_btn.place(x=700, y=425)

video_loop()

window.mainloop()
cv.close()
