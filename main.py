# coding: utf8
import Tkinter
from Tkinter import *
from polygon import *

point = []
polygon = []

canvas_height = 500
canvas_width = 500


# 清空画布
def clear():
    global point, polygon, C, canvas_height, canvas_width
    point = []
    polygon = []
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
    global point, polygon
    print event.x, event.y
    if len(point) > 0:
        if abs(event.x - point[0].x) + abs(event.y - point[0].y) < 10:
            C.create_line(point[0].x, point[0].y, point[-1].x, point[-1].y, fill='red')
            p = Polygon(point)
            Polygon.fill(C, p.paint())
            point = []
            polygon.append(p)
            for (a,b) in p.paint():
                print a,b
            return
        else:
            C.create_line(point[-1].x, point[-1].y, event.x, event.y, fill='red')
    point.append(Point(event.x, event.y))


top = Tk()
top.geometry('600x500')

C = Tkinter.Canvas(top, bg="gray", height=canvas_height, width=canvas_width)
C.pack(side=LEFT)

win = PanedWindow(top)
win.pack(side=RIGHT)

C.bind("<Button 1>", record_coordinate)

button1 = Button(win, text='清空', width=20, command=clear)
button1.pack()
button2 = Button(win, text='交集', width=20, command=merge)
button2.pack()
button3 = Button(win, text='立方体:关', width=20)
button3.pack()

top.mainloop()
