# coding: utf8


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    # 保证第一个点y值不低于第二个点
    def __init__(self, point_1, point_2):
        self.point_1 = point_1
        self.point_2 = point_2
        if self.point_1.y > self.point_2.y:
            self.point_1, self.point_2 = self.point_2, self.point_1
