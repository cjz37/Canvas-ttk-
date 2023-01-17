import time
import threading
import os
from PIL import Image, ImageTk, ImageGrab
import math
import random

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter.colorchooser as tkc
from tkinter.filedialog import askopenfilename, asksaveasfilename

import ini


class PaintApp(ttk.Window):
    def __init__(
        self,
        title='Sketch2Pose   V1.2beta',
        themename='darkly',
        iconphoto='icons/icon.png',
        size=(1280, 780),
        position=(100, 50),
        minsize=(960, 585),
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

        self.initParameters()
        self.setupUi()

        # Test
        self.test()

    def initParameters(self):
        self.theme_option_var = ttk.StringVar()
        self.yesno_var = ttk.IntVar(value=0)
        self.what_var = ttk.IntVar(value=1)
        self.x_var = ttk.IntVar(value=0)
        self.y_var = ttk.IntVar(value=0)
        self.image = ttk.PhotoImage()

        # 当前图层 id
        self.cur_layer = ttk.IntVar(value=1)  # index from 1
        # 图层总数
        self.layers_num = ttk.IntVar(value=1)
        # 图层 id 数组的当前索引
        self.layers_idList_idx = 0
        # 目前已申请到的图层 id
        self.layers_id = 1
        # 图层列表中的 id
        self.layers_idList = [1]
        # 图层信息
        self.layers = [[[0]]]
        # 上一次绘制申请的 item
        self.lastEnd = 1

        self.brushThickness_var = ttk.IntVar(value=0)
        self.foreColor = '#000000'
        self.backColor = '#FFFFFF'
        self.lastDraw = 0
        self.end = [0, 1]

        self.cur_theme = ini.load_ini()

# Test start ====================
    def test(self):
        self.Label_testArea = ttk.Label(
            self.LabelFrame_edit_bottom,
            text='----------------TestArea-----------------',
        ).pack(
            pady=2,
        )

        self.Label_cur_layer_label = ttk.Label(
            self.LabelFrame_edit_bottom,
            text='Cur layer id:',
        ).pack(
            pady=2,
        )
        self.Label_cur_layer = ttk.Label(
            self.LabelFrame_edit_bottom,
            text='0',
            textvariable=self.cur_layer,
        ).pack(
            pady=2,
        )
        self.Label_layers_num_label = ttk.Label(
            self.LabelFrame_edit_bottom,
            text='Layers num:',
        ).pack(
            pady=2,
        )
        self.Label_layers_num = ttk.Label(
            self.LabelFrame_edit_bottom,
            text='0',
            textvariable=self.layers_num,
        ).pack(
            pady=2,
        )
        self.Label1 = ttk.Label(
            self.LabelFrame_edit_bottom,
            text='------------------Move-------------------',
        ).pack(
            pady=2,
        )
        self.test_Button1 = ttk.Button(
            self.LabelFrame_edit_bottom,
            text='Move up',
            command=self.move_up,
        ).pack(
            pady=2,
        )
        self.test_Button2 = ttk.Button(
            self.LabelFrame_edit_bottom,
            text='Move down',
            command=self.move_down,
        ).pack(
            pady=2,
        )
        self.test_Button7 = ttk.Button(
            self.LabelFrame_edit_bottom,
            text='Move left',
            command=self.move_left,
        ).pack(
            pady=2,
        )
        self.test_Button8 = ttk.Button(
            self.LabelFrame_edit_bottom,
            text='Move right',
            command=self.move_right,
        ).pack(
            pady=2,
        )
        self.Label2 = ttk.Label(
            self.LabelFrame_edit_bottom,
            text='-------------Layers operate-------------',
        ).pack(
            pady=2,
        )
        self.test_Button3 = ttk.Button(
            self.LabelFrame_edit_bottom,
            text='Up',
            command=self.up,
        ).pack(
            pady=2,
        )
        self.test_Button4 = ttk.Button(
            self.LabelFrame_edit_bottom,
            text='Down',
            command=self.down,
        ).pack(
            pady=2,
        )
        self.Label3 = ttk.Label(
            self.LabelFrame_edit_bottom,
            text='---------------Parameters---------------',
        ).pack(
            pady=2,
        )
        self.test_Button5 = ttk.Button(
            self.LabelFrame_edit_bottom,
            text='Show end',
            command=self.show_end,
        ).pack(
            pady=2,
        )
        self.test_Button6 = ttk.Button(
            self.LabelFrame_edit_bottom,
            text='Show layers',
            command=self.show_layers,
        ).pack(
            pady=2,
        )

    def move_up(self):
        try:
            move_layer = self.layers[self.cur_layer.get()]
            l = len(move_layer)
            for idx in range(0, l):
                for item in range(move_layer[idx][0], move_layer[idx][1] + 1):
                    self.canvas.move(item, 0, -80)
        except:
            pass

    def move_down(self):
        try:
            move_layer = self.layers[self.cur_layer.get()]
            l = len(move_layer)
            for idx in range(0, l):
                for item in range(move_layer[idx][0], move_layer[idx][1] + 1):
                    self.canvas.move(item, 0, 80)
        except:
            pass

    def move_left(self):
        try:
            move_layer = self.layers[self.cur_layer.get()]
            l = len(move_layer)
            for idx in range(0, l):
                for item in range(move_layer[idx][0], move_layer[idx][1] + 1):
                    self.canvas.move(item, -80, 0)
        except:
            pass

    def move_right(self):
        try:
            move_layer = self.layers[self.cur_layer.get()]
            l = len(move_layer)
            for idx in range(0, l):
                for item in range(move_layer[idx][0], move_layer[idx][1] + 1):
                    self.canvas.move(item, 80, 0)
        except:
            pass

    # 下一个图层（后申请的）
    def up(self):
        try:
            self.cur_layer.set(self.layers_idList[self.layers_idList_idx + 1])
            self.layers_idList_idx += 1
        except:
            pass

    # 上一个图层
    def down(self):
        if self.layers_idList_idx > 0:
            self.cur_layer.set(self.layers_idList[self.layers_idList_idx - 1])
            self.layers_idList_idx -= 1

    def show_end(self):
        print('end: ', self.end)

    def show_layers(self):
        print('layers: ',  self.layers)
# Test end ====================

# UI start ====================
    def setupUi(self):
        # setup theme
        self.style.theme_use(self.cur_theme)

# Menu start ====================
        self.Menu_main = ttk.Menu(self)

        # File
        self.Menu_file = ttk.Menu(self)

        self.Menu_file.add_command(
            label='Import',
            command=self.import_file,
        )
        self.Menu_file.add_command(
            label='Save',
            command=self.save_file)
        self.Menu_file.add_separator()
        self.Menu_file.add_command(
            label='Open the recently generated model',
            command=self.open_model_thread,
        )

        self.Menu_main.add_cascade(
            label='File',
            menu=self.Menu_file,
        )

        # Edit
        self.Menu_edit = ttk.Menu(self)

        self.Menu_edit.add_command(
            label='Revoke',
            command=self.revoke,
        )
        self.Menu_edit.add_command(
            label='Clear screen',
            command=self.clear_screen)

        self.Menu_main.add_cascade(
            label='Edit',
            menu=self.Menu_edit,
        )

        # Tools
        self.Menu_tools = ttk.Menu(self)

        self.Menu_tools.add_command(
            label='Pencil',
            command=self.draw_curve,
        )
        self.Menu_tools.add_command(
            label='Line',
            command=self.draw_line,
        )
        self.Menu_tools.add_command(
            label='Rectangle',
            command=self.draw_rectangle,
        )
        self.Menu_tools.add_command(
            label='Circle',
            command=self.draw_circle,
        )
        self.Menu_tools.add_command(
            label='Erase',
            command=self.on_erase,
        )
        self.Menu_tools.add_separator()
        self.Menu_tools.add_command(
            label='Choose forecolor',
            command=self.choose_foreColor,
        )
        self.Menu_tools.add_command(
            label='Choose backcolor',
            command=self.choose_backColor,
        )

        self.Menu_main.add_cascade(
            label='Tools',
            menu=self.Menu_tools,
        )

        # Func
        self.Menu_func = ttk.Menu(self)

        self.Menu_func.add_command(
            label='Generate',
            command=self.generate_thread,
        )

        self.Menu_main.add_cascade(
            label='Func',
            menu=self.Menu_func,
        )

        # Theme
        self.Menu_theme = ttk.Menu(self)

        for option in ['litera',
                       'minty',
                       'morph',
                       'superhero',
                       'solar',
                       'darkly',
                       'cyborg',
                       'vapor']:
            self.Menu_theme.add_radiobutton(
                label=option,
                value=option,
                variable=self.theme_option_var,
                command=self.set_style,
            )
        self.theme_option_var.set(self.cur_theme)

        self.Menu_main.add_cascade(
            label='Theme',
            menu=self.Menu_theme,
        )

        self['menu'] = self.Menu_main
# Menu end ====================

# Operate area start ====================
# Main area
        self.Frame_main = ttk.Frame(self)
        self.Frame_main.pack(
            side=TOP,
            padx=4,
            pady=6,
            fill=BOTH,
            expand=True,
        )

# edit area
        self.Frame_edit = ttk.Frame(self.Frame_main)
        self.Frame_edit.pack(
            side=LEFT,
            fill=Y,
        )

# Color selector Frame
        self.LabelFrame_edit_top = ttk.Labelframe(
            self.Frame_edit,
            text='Color&Brush',
        )
        self.LabelFrame_edit_top.pack(
            side=TOP,
            fill=X,
            padx=2,
        )

        # DEMO Combobox
        self.Combobox_test1 = ttk.Combobox(
            self.LabelFrame_edit_top,
            # bootstyle=DANGER,
            font=('yahe', 12),
            values=['red', 'blue', 'yellow'],
        )
        self.Combobox_test1.current(1)
        self.Combobox_test1.pack(
            padx=10,
            pady=10,
        )

        # Scale Frame: edit brush's & erase's size
        self.Frame_scale = ttk.Frame(self.LabelFrame_edit_top)
        self.Frame_scale.pack(
            side=TOP,
            fill=X,
        )
        # Lable of Scale
        self.Label_cur_toolName = ttk.Label(
            self.Frame_scale,
            text='Brush',
            width=6,
        )
        self.Label_cur_toolName.pack(
            side=LEFT,
            padx=10,
        )

        # Scale
        self.Scale_test1 = ttk.Scale(
            self.Frame_scale,
            orient=HORIZONTAL,
            value=0,
            from_=0,
            to=10,
            variable=self.brushThickness_var
        ).pack(
            fill=X,
            padx=10,
            pady=10,
        )

# Layers Frame
        self.LabelFrame_edit_bottom = ttk.LabelFrame(
            self.Frame_edit,
            text='Layers',
        )
        self.LabelFrame_edit_bottom.pack(
            side=BOTTOM,
            fill=BOTH,
            expand=True,
            padx=2,
        )

        self.Frame_buttonArea = ttk.Frame(
            self.LabelFrame_edit_bottom,
        )
        self.Frame_buttonArea.pack(
            side=TOP,
            fill=X,
            padx=2,
            pady=2,
        )

        self.Button_add_layers = ttk.Button(
            self.Frame_buttonArea,
            text='Add layer',
            command=self.add_layer,
        )
        self.Button_add_layers.pack(
            side=LEFT,
            # fill=X,
            padx=4,
            pady=4,
        )

        self.Button_delete_layers = ttk.Button(
            self.Frame_buttonArea,
            text='Delete the layer',
            command=self.del_cur_layer,
        )
        self.Button_delete_layers.pack(
            side=LEFT,
            # fill=X,
            padx=4,
            pady=4,
        )

# canvas area
        self.LabelFrame_canvas = ttk.LabelFrame(
            self.Frame_main,
            text='Canvas',)
        self.LabelFrame_canvas.pack(
            side=LEFT,
            fill=BOTH,
            expand=True,
            padx=2,
        )

        self.canvas = ttk.Canvas(
            self.LabelFrame_canvas,
            bg='#FFFFFF',
            cursor='circle',
        )
        self.canvas.pack(
            fill=BOTH,
            expand=YES,
        )

        self.canvas.create_rectangle(
            0, 0, 6000, 6000, fill='#dddddd', outline='white')

        self.canvas.bind('<Button-1>', self.onLeftButton_down)
        self.canvas.bind('<B1-Motion>', self.onLeftButton_move)
        self.canvas.bind('<ButtonRelease-1>', self.onLeftButton_up)
        self.canvas.bind('<ButtonRelease-3>', self.onRightButton_up)
# Operate area start ====================
# UI end ====================

# Functions start ====================
# UI functions start ====================
    def set_style(self):
        self.cur_theme = self.theme_option_var.get()
        self.style.theme_use(self.cur_theme)
        ini.update_ini(self.cur_theme)

    def getter(self):
        time.sleep(0.5)
        x = self.winfo_x() + self.canvas.winfo_x()
        y = self.winfo_y() + self.canvas.winfo_y()
        if self.winfo_x() < 0:
            x = 0
        if self.winfo_y() < 0:
            y = 0
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        currentPath = os.getcwd()
        targetPath = '\\data\\images'
        uuid_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
        temp_fileName = '%s' % uuid_str
        ext = ttk.StringVar()
        path = asksaveasfilename(
            initialfile=temp_fileName,
            typevariable=ext,
            filetypes=[('JPEG image', '*.jpg *.jpeg *.jpe'),
                       ('PNG image', '*.png'),
                       ('Photoshop image', '*.psd')],
            initialdir=(currentPath + targetPath),
        )

        if not path:
            return False

        fileFormat = ttk.StringVar()
        if ext.get() == 'JPEG image':
            fileFormat = '.jpg'
        if ext.get() == 'PNG image':
            fileFormat = '.png'
        if ext.get() == 'Photoshop image':
            fileFormat = '.psd'
        print('save path: ', path + fileFormat)
        x_add = 240
        y_add = 57
        if self.winfo_width() > 1900:
            y_add = 70
        if self.winfo_width() < 960:
            x_add = 255
        ImageGrab.grab().crop((x+x_add, y+y_add, x1+227, y1+55)).save(path + fileFormat)
        self.generate_cmd(path + fileFormat)
        self.open_cmd(temp_fileName)
        return True

    def import_file(self):
        path = askopenfilename(
            title='Import file',
            filetypes=[('All supported formats', '*.jpg *.png')]
        )
        print(path)
        if path:
            self.image = Image.open(path)
            w = self.image.width
            h = self.image.height
            self.image = self.image.resize((int(600 / h * w), 600))
            self.image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(400, 300, image=self.image)
        else:
            return

    def save_file(self):
        self.getter()

    def revoke(self):
        print('cur layer revoke')
        try:
            for item in range(self.layers[self.cur_layer.get()][-1][0],
                              self.layers[self.cur_layer.get()][-1][1] + 1):
                self.canvas.delete(item)
            self.layers[self.cur_layer.get()].pop()
        except:
            pass

    def clear_screen(self):
        print('clear screen')
        try:
            clear_layer = self.layers[self.cur_layer.get()]
            self.layers[self.cur_layer.get()] = []
            l = len(clear_layer)
            for idx in range(0, l):
                for item in range(clear_layer[idx][0], clear_layer[idx][1] + 1):
                    self.canvas.delete(item)
        except:
            pass

    def draw_curve(self):
        self.Label_cur_toolName.config(text='Brush')
        self.what_var.set(1)

    def draw_line(self):
        self.Label_cur_toolName.config(text='Brush')
        self.what_var.set(2)

    def draw_rectangle(self):
        self.Label_cur_toolName.config(text='Brush')
        self.what_var.set(3)

    def draw_circle(self):
        self.Label_cur_toolName.config(text='Brush')
        self.what_var.set(4)

    def on_erase(self):
        self.Label_cur_toolName.config(text='Erase')
        self.what_var.set(5)

    def choose_foreColor(self):
        self.foreColor = tkc.askcolor()[1]

    def choose_backColor(self):
        self.backColor = tkc.askcolor()[1]

    def onLeftButton_down(self, event):
        self.yesno_var.set(1)
        self.x_var.set(event.x)
        self.y_var.set(event.y)

    def onLeftButton_move(self, event):
        if self.yesno_var.get() == 0:
            return
        # pencil
        if self.what_var.get() == 1:
            self.lastDraw = self.canvas.create_line(
                self.x_var.get(),
                self.y_var.get(),
                event.x,
                event.y,
                width=self.brushThickness_var.get(),
                fill=self.foreColor,
            )

            self.x_var.set(event.x)
            self.y_var.set(event.y)
        # line
        elif self.what_var.get() == 2:
            try:
                self.canvas.delete(self.lastDraw)
            except Exception:
                pass

            self.lastDraw = self.canvas.create_line(
                self.x_var.get(),
                self.y_var.get(),
                event.x,
                event.y,
                fill=self.foreColor,
            )
        # rectangle
        elif self.what_var.get() == 3:
            try:
                self.canvas.delete(self.lastDraw)
            except Exception:
                pass
            self.lastDraw = self.canvas.create_rectangle(
                self.x_var.get(),
                self.y_var.get(),
                event.x,
                event.y,
                # fill=self.backColor,
                outline=self.foreColor,
            )
        # circle
        elif self.what_var.get() == 4:
            try:
                self.canvas.delete(self.lastDraw)
            except Exception:
                pass
            self.lastDraw = self.canvas.create_oval(
                self.x_var.get(),
                self.y_var.get(),
                event.x,
                event.y,
                # fill=self.backColor,
                outline=self.foreColor,
            )
        # erase
        elif self.what_var.get() == 5:
            self.lastDraw = self.canvas.create_rectangle(
                event.x - (self.brushThickness_var.get() + 1) * 10,
                event.y - (self.brushThickness_var.get() + 1) * 10,
                event.x + (self.brushThickness_var.get() + 1) * 10,
                event.y + (self.brushThickness_var.get() + 1) * 10,
                fill=self.backColor,
                outline=self.backColor,
            )

    def onLeftButton_up(self, event):
        if self.what_var.get() == 2:
            self.lastDraw = self.canvas.create_line(
                self.x_var.get(),
                self.y_var.get(),
                event.x,
                event.y,
                fill=self.foreColor,
            )
        elif self.what_var.get() == 3:
            self.lastDraw = self.canvas.create_rectangle(
                self.x_var.get(),
                self.y_var.get(),
                event.x,
                event.y,
                outline=self.foreColor,
            )
        elif self.what_var.get() == 4:
            self.lastDraw = self.canvas.create_oval(
                self.x_var.get(),
                self.y_var.get(),
                event.x,
                event.y,
                outline=self.foreColor,
            )
        self.yesno_var.set(0)
        # self.end.append([self.end[len(self.end) - 1][1] + 1, self.lastDraw])
        self.end = [self.lastEnd + 1, self.lastDraw]
        self.lastEnd = self.lastDraw
        try:
            self.layers[self.cur_layer.get()].append(self.end)
        except:
            self.layers.append([self.end])

    def onRightButton_up(self, event):
        self.Menu_tools.post(
            event.x_root,
            event.y_root,
        )

    def add_layer(self):
        print('add layer')
        self.layers_num.set(self.layers_num.get() + 1)

        self.layers_id += 1
        self.layers_idList_idx += 1
        self.layers_idList.insert(self.layers_idList_idx, self.layers_id)
        self.cur_layer.set(self.layers_idList[self.layers_idList_idx])

    def del_cur_layer(self):
        if self.layers_num.get() > 1:
            print('delete the layer')
            self.clear_screen()

            self.layers_num.set(self.layers_num.get() - 1)
            self.layers_idList.remove(self.cur_layer.get())
            try:
                self.cur_layer.set(self.layers_idList[self.layers_idList_idx])
            except:
                self.layers_idList_idx -= 1
                self.cur_layer.set(self.layers_idList[self.layers_idList_idx])

        else:
            print('can not delete')

    # 保存当前图层信息
    def save_cur_layer(self):
        try:
            self.layers[self.cur_layer.get()].append(self.end)
        except:
            self.layers.append(self.end)

# UI functions end ====================

# Func start ====================
    def generate_cmd(self, image_path):
        # cmd = 'python src/pose.py --save-path output --img-path ' + \
        #       image_path + ' --use-cos --use-angle-transf --use-natural'
        # file = open('run.bat', 'w', encoding='utf-8')
        # file.write(cmd)
        # file.close()
        print('save image and create run.bat')

    def open_cmd(self, image_name):
        # cmd = 'python open3dmodel.py --image-name ' + image_name
        # file = open('open.bat', 'w', encoding='utf-8')
        # file.write(cmd)
        # file.close()
        print('create open.bat')

    def open_model(self):
        # os.system('open.bat')
        print('open model')

    # thread of opening 3d model

    def open_model_thread(self):
        # thread = threading.Thread(target=open_model, args=())
        # thread.start()
        print('open model thread')

    def run(self):
        if self.getter(self.canvas):
            print('generating...')
            # os.system('run.bat')
            print('The model has been successfully generated!')
            # open_model()

    # thread of running pose.py
    def generate_thread(self):
        # thread = threading.Thread(target=run, args=())
        # thread.start()
        print('run pose.py thread')
# Func end ====================
# Functions end ====================


if __name__ == '__main__':
    mainWindow = PaintApp()
    mainWindow.mainloop()
