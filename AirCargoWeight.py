try:
    import Tkinter as tk
    from Tkinter.ttk import *
    from Tkinter import *
    from Tknter import filedialog, Menu

except ImportError: # Python 3
    import tkinter as tk
    from tkinter.ttk import *
    from tkinter import *
    from tkinter import filedialog, Menu
    from tkinter.messagebox import showinfo

from functools import reduce
from itertools import combinations
import numpy as np

#--- 錯誤Label處理 ---#
def label_error(string):
    result_label.configure(text=string, foreground='red')

#--- 計算配重 ---#
def josh_calculate():

    if str(weight_entry.get()).strip('') == '':
        label_error('Weight list is empty')
        return

    if str(goal_entry.get()).strip('') == '':
        label_error('Goal is empty')
        return

    if str(pick_entry.get()).strip('') == '':
        label_error('Pick Count is empty')
        return

    #--- 取得配重清單並處理 ---#
    getList = weight_entry.get().split(',')
    list_ = [float(x) for x in getList]

    #--- 取得目標重 ---#
    goal = float(goal_entry.get())

    #--- 取得挑選數量 ---#
    pick_num = int(pick_entry.get())

    #--- 按照餘數小的排序 ---#
    def func(x):
        return x % (goal/pick_num)

    #--- 依照func定義規則排序重量清單 ---#
    list_.sort(key=func)

    #--- 去除掉多餘的0 ---#
    def floatable(x):
        if x == int(x):
            return int(x)
        else:
            return x

    #--- 判斷是否成功 ---#
    success = False

    #--- 利用combinations迭代重量清單 ---#
    for item in combinations(list_, pick_num):

        #--- 看看迭代出來的結果是否符合目標重量，有符合就跳出 ---#
        if float(np.sum(item)) == float(goal):

            #--- 設置成功標籤 ---#
            success = True

            #--- 將item中物件轉換為float ---#
            item_r = [floatable(x) for x in item]

            #--- 結果文字設置 ---#
            result = 'Answer：{}'.format(item_r)
            #--- 將結果代入Label ---#
            result_label.configure(text=result, foreground='black')
            break

    #--- 沒有任何一筆符合，輸出錯誤訊息 ---#
    if success is False:
        label_error(string='Can not reach the goal weight。。')

#--- 複製剪貼板 ---#
def clipping():

    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(str(result_label.cget("text")).strip('Answer：').strip('[').strip(']'))
    r.update()
    r.destroy()

window = tk.Tk()
window.title('Air Cargo App')
window.configure(background='white')

#--- 窗口尺寸 ---#
window.geometry('500x300')

#--- 標題初始化 ---#
header_label = tk.Label(window, text='Air Cargo Weight Counter', width='500', height='4', font=('Helvetica-Light', 15))
header_label.pack()

#--- 重量清單向上對齊父元件 ---#
weight_frame = tk.Frame(window)
weight_frame.pack(side=tk.TOP)
weight_label = tk.Label(weight_frame, text='Weight List：', font='Helvetica-Light')
weight_label.pack(side=tk.LEFT)
weight_entry = tk.Entry(weight_frame)
weight_entry.pack(side=tk.LEFT)

#--- 目標值初始化 ---#
goal_frame = tk.Frame(window)
goal_frame.pack(side=tk.TOP)
goal_label = tk.Label(goal_frame, text='Goal：', font='Helvetica-Light')
goal_label.pack(side=tk.LEFT)
goal_entry = tk.Entry(goal_frame)
goal_entry.pack(side=tk.LEFT)

#--- 挑選數量初始化 ---#
pick_frame = tk.Frame(window)
pick_frame.pack(side=tk.TOP)
pick_label = tk.Label(pick_frame, text='Pick Count：', font='Helvetica-Light')
pick_label.pack(side=tk.LEFT)
pick_entry = tk.Entry(pick_frame)
pick_entry.pack(side=tk.LEFT)

#--- 結果顯示 ---#
result_label = tk.Label(window, width=50, height=3)
result_label.pack()

#--- 開始計算按鈕生成 ---#
calculate_btn = tk.Button(window, text='Start', command=josh_calculate, width='30', height='2', font='Helvetica-Light')
calculate_btn.pack()

#--- 複製結果按鈕生成 ---#
clip_btn = tk.Button(window, text='Copy', command=clipping, width='30', height='2', font='Helvetica-Light')
clip_btn.pack()

window.mainloop()
