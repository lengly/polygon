# coding: utf8
import copy


class Point:
    def __init__(self, x, y):
        self.x = int(round(x))
        self.y = int(round(y))

    def __str__(self):
        return str(self.x) + ', ' + str(self.y)


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        if p1.y == p2.y:
            self.delta = 0
        else:
            self.delta = float(p1.x - p2.x) / (p1.y - p2.y)
        self.x = p1.x if p1.y < p2.y else p2.x
        self.yMax = max(p1.y, p2.y)
        self.yMin = min(p1.y, p2.y)


class Polygon:
    # 构造出线  并记录下多边形y坐标轴的区间范围
    def __init__(self, point):
        self.line = []
        self.yMin = point[-1].y
        self.yMax = point[-1].y
        for i in range(len(point) - 1):
            self.line.append(Line(point[i], point[i+1]))
            self.yMin = min(self.yMin, point[i].y)
            self.yMax = max(self.yMax, point[i].y)
        if len(point) > 2:
            self.line.append(Line(point[0], point[-1]))

    # 填充多边形颜色 返回区间
    def paint(self):
        ret = []
        net = {}
        # 初始化新边表头指针net
        for line in self.line:
            if line.yMin not in net:
                net[line.yMin] = []
            net[line.yMin].append(copy.deepcopy(line))
        aet = []
        for y in range(self.yMin, self.yMax + 1):
            # 把新边表net[line]中的边节点加入aet表中  使之按x坐标递增排序
            if y in net:
                aet.extend(net[y])
            aet.sort(lambda a,b: cmp(a.x, b.x))
            i = 0
            if y in net:
                while i < len(aet) - 1:
                    if abs(aet[i].x - aet[i+1].x) < 1e-5:
                        if aet[i+1].yMin < y:
                            aet.pop(i+1)
                        if aet[i].yMin < y:
                            aet.pop(i)
                    i += 1
            for i in range(0, len(aet) - 1, 2):
                ret.append([Point(aet[i].x, y), Point(aet[i+1].x, y)])
            aet = [w for w in aet if w.yMax > y]
            for w in aet:
                w.x += w.delta
        return ret

    # 根据区间填充颜色
    @staticmethod
    def fill(canvas, interval, color='red'):
        for (a, b) in interval:
            canvas.create_line(a.x, a.y, b.x, b.y, fill=color)

    # 根据两个多边形的区间求交
    @staticmethod
    def merge(list_a, list_b):
        compare = lambda a, b: (a[0].y < b[0].y) or ((a[0].y == b[0].y) and (a[1].x < b[1].x))
        ret = []
        while (len(list_a) > 0) and (len(list_b) > 0):
            a = list_a[0]
            b = list_b[0]
            point_1 = Point(max(a[0].x, b[0].x), a[0].y)
            point_2 = Point(min(a[1].x, b[1].x), a[1].y)
            if (a[0].y == b[0].y) and (point_1.x < point_2.x):
                ret.append([point_1, point_2])
            if compare(a, b):
                list_a.pop(0)
            else:
                list_b.pop(0)

        return ret
