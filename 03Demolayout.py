'''
Author: Crange 839704627@qq.com
Date: 2023-01-13 16:01:59
LastEditors: Crange 839704627@qq.com
LastEditTime: 2023-01-17 20:52:14
'''
import tkinter
import ttkbootstrap as ttk



root = ttk.Window()

f1=tkinter.Frame(root)
f1.pack(side=tkinter.TOP,pady=2,fill=tkinter.X) #横向占满空间
tkinter.Button(f1,width=3,text='File').pack(side=tkinter.LEFT,)#以 f1 做为容器
tkinter.Button(f1,width=3,text='Edit').pack(side=tkinter.LEFT,)#以 f1 做为容器

f2=tkinter.Frame(root)
f2.pack(side=tkinter.TOP,pady=2,fill=tkinter.X)

f4=tkinter.Frame(f2) #以 f2 做为容器
f4.pack(side=tkinter.TOP,fill=tkinter.X)

f8=tkinter.Frame(f4) #以 f4 做为容器
f8.pack(side=tkinter.LEFT,fill=tkinter.Y) #纵向占满空间
tkinter.Label(text="……\n……").pack(padx=2)#控制前后间隔，不设宽度会根据文本长度自行调整

f9=tkinter.Frame(f4)
f9.pack(side=tkinter.LEFT,fill=tkinter.Y)

f12=tkinter.Frame(f9) #以 f9 做为容器
f12.pack(side=tkinter.TOP,pady=2,fill=tkinter.X)
tkinter.Radiobutton(f12,text="……").pack(side=tkinter.LEFT,padx=2)#以 f12 做为容器
ttk.Combobox(f12,width=20).pack(side=tkinter.LEFT,padx=2) #用 width 控制长度
ttk.Combobox(f12).pack(side=tkinter.LEFT,padx=2,fill=tkinter.X) #可先其中一小部件充满剩余空间，使界面好看些

f13=tkinter.Frame(f9) #以 f9 做为容器
f13.pack(side=tkinter.TOP,pady=2,fill=tkinter.X)
    #……
tkinter.Entry(f13).pack(side=tkinter.LEFT,fill=tkinter.X)#以 f13 做为容器

f5=tkinter.Frame(f2) #以 f2 做为容器
f5.pack(side=tkinter.TOP,fill=tkinter.X)
    	#……

f3=tkinter.Frame(root)
f3.pack(side=tkinter.TOP,pady=2,fill=tkinter.BOTH,expand=True) #充满窗体剩余空间

f6=tkinter.LabelFrame(f3,text="书目结构") #以 f3 做为容器
f6.pack(side=tkinter.LEFT,fill=tkinter.Y)#纵向占满空间

f10=tkinter.Frame(f6) #以 f6 做为容器
f10.pack(side=tkinter.TOP,fill=tkinter.X)

f11=tkinter.Frame(f6) #以 f6 做为容器
f11.pack(side=tkinter.TOP,fill=tkinter.BOTH,expand=True)#占满剩余空间

f7=tkinter.LabelFrame(f3,text="内容预览") #以 f3 做为容器
f7.pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)#纵向占满空间

tkinter.Scrollbar(f7,orient=tkinter.VERTICAL).pack(side=tkinter.RIGHT,fill=tkinter.Y)#先布局，避免有时被挤掉
tkinter.Text(f7).pack(side=tkinter.LEFT,fill=tkinter.BOTH,expand=True)#占满剩余空间

    
tkinter.Text(height=2).pack(side=tkinter.TOP,fill=tkinter.X,pady=2) #仅1个小部件，所以省掉 Frame 直接使用小部件


root.mainloop()
