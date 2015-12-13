# coding: utf8
import math
from polygon import *
import copy


class Point3D:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

    def to_2d(self, mid_x, mid_y):
        return Point(self.z + mid_x, self.y + mid_y)

    def __str__(self):
        return str(self.x) + ', ' + str(self.y) + ', ' + str(self.z)


class Plane:
    def __init__(self, point, color):
        self.point = point
        self.color = color

    def get_x(self):
        return min(min(self.point[0].x, self.point[1].x), min(self.point[2].x, self.point[3].x))

    def get_polygon(self, mid_x, mid_y):
        return Polygon(map(lambda x: x.to_2d(mid_x, mid_y), self.point))

    def __str__(self):
        return ', '.join(map(lambda x: str(x), self.point))


class Cube:
    def __init__(self):
        self.theta = 1.0 * math.pi / 180.0

        r = 50.0
        self.point = []
        self.point.append(Point3D( r,  r, -r))
        self.point.append(Point3D( r,  r,  r))
        self.point.append(Point3D( r, -r,  r))
        self.point.append(Point3D( r, -r, -r))
        self.point.append(Point3D(-r,  r, -r))
        self.point.append(Point3D(-r,  r,  r))
        self.point.append(Point3D(-r, -r,  r))
        self.point.append(Point3D(-r, -r, -r))

        self.backup = copy.deepcopy(self.point)

    # 绕Y轴旋转
    def rotate_y(self, towards):
        sin_theta = math.sin(self.theta * towards)
        cos_theta = math.cos(self.theta * towards)
        for p in self.point:
            p.x, p.z = cos_theta * p.x + sin_theta * p.z, -sin_theta * p.x + cos_theta * p.z


    # 绕Z轴旋转
    def rotate_z(self, towards):
        sin_theta = math.sin(self.theta * towards)
        cos_theta = math.cos(self.theta * towards)
        for p in self.point:
            p.x, p.y = cos_theta * p.x - sin_theta * p.y, sin_theta * p.x + cos_theta * p.y

    # 画
    def paint(self, canvas, mid_x, mid_y):
        plane = list()
        plane.append(Plane([self.point[0], self.point[1], self.point[2], self.point[3]], '#ff0000'))
        plane.append(Plane([self.point[0], self.point[1], self.point[5], self.point[4]], '#00ff00'))
        plane.append(Plane([self.point[0], self.point[3], self.point[7], self.point[4]], '#0000ff'))
        plane.append(Plane([self.point[1], self.point[2], self.point[6], self.point[5]], '#ffff00'))
        plane.append(Plane([self.point[2], self.point[3], self.point[7], self.point[6]], '#ff00ff'))
        plane.append(Plane([self.point[4], self.point[5], self.point[6], self.point[7]], '#00ffff'))

        plane.sort(cmp=lambda a, b: cmp(a.get_x(), b.get_x()))
        for p in plane:
            Polygon.fill(canvas, p.get_polygon(mid_x, mid_y).paint(), p.color)