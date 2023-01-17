'''
Author: Crange 839704627@qq.com
Date: 2023-01-15 21:54:15
LastEditors: Crange 839704627@qq.com
LastEditTime: 2023-01-17 20:52:02
'''
import time
import threading
import os
from PIL import Image, ImageTk, ImageGrab

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.colorchooser as tkc
from tkinter.filedialog import askopenfilename, asksaveasfilename

import ini

class test(ttk.Window):
    def __init__(
        self,
        title='Sketch2Pose   V1.2beta',
        themename='darkly',
        iconphoto='icons/icon.png',
        size=(1280, 780),
        position=(100, 50),
        minsize=(495, 630),
        maxsize=None,
        resizable=None,
        hdpi=True,
        scaling=None,
        transient=None,
        overrideredirect=False,
        alpha=1
    ):
        super().__init__(
            title,
            themename,
            iconphoto,
            size,
            position,
            minsize,
            maxsize,
            resizable,
            hdpi,
            scaling,
            transient,
            overrideredirect,
            alpha
        )

        self.isShow = 1
        self.rect = []


    def setupUi(self):
        # 创建画布对象
        self.canvas = tk.Canvas(self, bg="blue", height=440, width=440)
        self.img = Image.open("./icons/icon.png").resize([440, 440]) # 打开图片
        self.photo = ImageTk.PhotoImage(self.img)  # 使用ImageTk的PhotoImage方法
        # 安置图片在画布上面
        """0,0其实代表着我们放置图片的具体;
        位置anchor="nw"代表着原点位置;
        image代表图片对象是谁"""
        self.image = self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        # 定义画的图形大小，由它的初始坐标和终点坐标决定大小
        x1, y1, x2, y2 = 0, 0, 80, 80
        # 线条，fill参数代表颜色
        self.line = self.canvas.create_line(x1, y1, x2, y2, fill="red")
        # 画圆
        self.oval = self.canvas.create_oval(x1, y1, x2, y2, fill="yellow")
        # 画半圆,start参数代表开始的角度，extent代表最后的角度，所有画出一个半圆
        self.arc = self.canvas.create_arc(x1 + 30, y1 + 30, x2 + 30, y2 + 30, start=0, extent=180)
        # 矩形
        self.rect.append(self.canvas.create_rectangle(x1 + 10, y1 + 10, x2 + 10, y2 + 10))
        self.rect.append(self.canvas.create_rectangle(x1 + 10, y1 + 10, x2 + 200, y2 + 200))

        self.canvas.pack()

        self.b1 = tk.Button(window, text="move", command=self.moveit).pack()
        self.b2 = tk.Button(window, text="hidden&show", command=self.hidden_show).pack()
 


    # 定义移动函数
    def moveit(self):
        self.canvas.move(self.rect[0], 0, 3)

    def hidden_show(self):
        global iShow
        if iShow:
            self.canvas.itemconfig(self.oval, state='hidden')
            iShow = 0
        else:
            self.canvas.itemconfig(self.oval, state='normal')
            iShow = 1

    
if __name__ == '__main__':
    window = test()
    window.mainloop()