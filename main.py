# coding: utf8
import Tkinter
from Tkinter import *
from cube import *

point = []
polygon = []

canvas_height = 500
canvas_width = 500

mode = 0  # 0代表当前是非立方体模式 1代表当前是立方体模式
cube = None

x = 0
y = 0
delta_x = 0
delta_y = 0


# 清空画布
def clear():
    global point, polygon, C, canvas_height, canvas_width
    point = []
    polygon = []
    C.delete(ALL)
    for y in range(canvas_height):
        C.create_line(0, y, canvas_width, y, fill='gray')


# 求多边形的交
def merge():
    global polygon, C
    base = []
    for y in range(canvas_height):
        C.create_line(0, y, canvas_width, y, fill='gray')
        base.append([Point(0, y), Point(canvas_width, y)])
    for p in polygon:
        base = Polygon.merge(base, p.paint())
    for (a, b) in base:
        C.create_line(a.x, a.y, b.x, b.y, fill='red')


# 鼠标点击画线
def record_coordinate(event):
    global point, polygon, mode
    if mode == 1:
        return
    if len(point) > 0:
        if abs(event.x - point[0].x) + abs(event.y - point[0].y) < 10:
            C.create_line(point[0].x, point[0].y, point[-1].x, point[-1].y, fill='red')
            p = Polygon(point)
            Polygon.fill(C, p.paint())
            point = []
            polygon.append(p)
            return
        else:
            C.create_line(point[-1].x, point[-1].y, event.x, event.y, fill='red')
    point.append(Point(event.x, event.y))


# 点击立方体按钮 切换状态
def switch():
    global mode, cube, delta_x, delta_y
    clear()
    if mode == 1:
        mode = 0
        button3.config(text='立方体:关')
    else:
        mode = 1
        button3.config(text='立方体:开')
        delta_x = 0
        delta_y = 0
        cube = Cube()
        cube.rotate_y(45)
        cube.rotate_z(45)
        clear()
        cube.paint(C, canvas_width / 2, canvas_height / 2)


def start_move(event):
    global x, y, mode
    if mode == 0:
        record_coordinate(event)
        return
    x = event.x
    y = event.y


def stop_move(event):
    global x, y
    x = 0
    y = 0


def moving(event):
    global x, y, cube, mode, canvas_height, canvas_width, delta_x, delta_y
    if mode == 0:
        return
    delta_x = event.x - x
    delta_y = event.y - y

    cube.rotate_y(-delta_x)
    cube.rotate_z(delta_y)
    x = event.x
    y = event.y
    clear()
    cube.paint(C, canvas_width / 2, canvas_height / 2)


top = Tk()
top.geometry('600x500')

C = Tkinter.Canvas(top, bg="gray", height=canvas_height, width=canvas_width)
C.pack(side=LEFT)

win = PanedWindow(top)
win.pack(side=RIGHT)

C.bind("<Button 1>", record_coordinate)
C.bind('<ButtonPress-1>', start_move)
C.bind('<ButtonRelease-1>', stop_move)
C.bind('<B1-Motion>', moving)

button1 = Button(win, text='清空', width=20, command=clear)
button1.pack()
button2 = Button(win, text='交集', width=20, command=merge)
button2.pack()
button3 = Button(win, text='立方体:关', width=20, command=switch)
button3.pack()

top.mainloop()
