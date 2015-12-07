# coding: utf8
import Tkinter
from Tkinter import *
import polygon as P

top = Tk()
top.geometry('500x500')

C = Tkinter.Canvas(top, bg="gray", height=500, width=500)
C.pack(side=LEFT)

point = []


# 鼠标点击画线
def record_coordinate(event):
    print event.x,event.y
    if len(point) > 0:
        if abs(event.x - point[0].x) + abs(event.y - point[0].y) < 10:
            C.create_line(point[0].x, point[0].y, point[-1].x, point[-1].y, fill='red')
            return
        else:
            C.create_line(point[-1].x, point[-1].y, event.x, event.y, fill='red')
    point.append(P.Point(event.x, event.y))

C.bind("<Button 1>", record_coordinate)


top.mainloop()
