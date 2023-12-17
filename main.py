import re

import plotly.graph_objects as go
from kivy.uix.textinput import TextInput
from math import floor
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory

import os

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class IntegerInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super().insert_text(s, from_undo=from_undo)


def draw(points):
    x = []
    y = []
    points = list(set(points))
    for point in points:
        x.append(point.x)
        y.append(point.y)
    fig = go.Figure(go.Histogram2d(
        x=x,
        y=y,
        xaxis="x",
        yaxis="y",
        coloraxis="coloraxis",
        xbins={'start': min(x + y) - 5, 'size': 1, "end": max(x + y) + 5},
        ybins={'start': min(x + y) - 5, 'size': 1, "end": max(y + x) + 5}),
    )
    fig.update_layout(
        xaxis=dict(ticks='', showgrid=False, zeroline=False, nticks=20),
        yaxis=dict(ticks='', showgrid=False, zeroline=False, nticks=20),
        autosize=False,
        height=550,
        width=550,
        hovermode='closest',
    )
    fig.show()


def symmetric_add(x, y, shift_x, shift_y, tiles_1):
    tiles = [Point(x, y), Point(-x, y), Point(x, -y), Point(-x, -y)]

    temp_tiles = [Point(t.y, t.x) for t in tiles]

    tiles.extend(temp_tiles)

    for i in range(8):
        tiles[i].x += shift_x
        tiles[i].y += shift_y

    tiles_1.extend(tiles)


class Root(FloatLayout):
    def dismiss_popup(self):
        self._popup.dismiss()

    def it_method(self):
        f = Point(self.x1, self.y1)
        s = Point(self.x2, self.y2)
        if f.x > s.x:
            f, s = s, f
        dx = s.x - f.x
        dy = s.y - f.y
        result = [Point(s.x, s.y)]
        if dx == 0 and dy == 0:
            return result
        if abs(dx) >= abs(dy):
            a = dy / dx
            x, y = (f.x, f.y) if f.x <= s.x else (s.x, s.y)
            sgn = 1 if f.y > s.y else -1
            while x < s.x:
                result.append(Point(round(x), round(y)))
                x += 1
                y += a
        else:
            a = dx / dy
            x, y = (f.x, f.y) if f.y <= s.y else (s.x, s.y)
            sgn = 1 if f.x > s.x else -1
            while y < s.y:
                result.append(Point(round(x), round(y)))
                y += 1
                x += a
        draw(result)

    def dda_method(self):
        f = Point(self.x1, self.y1)
        s = Point(self.x2, self.y2)
        l = max(abs(s.x - f.x), abs(s.y - f.y))
        x, y = f.x, f.y
        L = l
        result = []
        while l > 0:
            result.append(Point(round(x), round(y)))
            x += (s.x - f.x) / L
            y += (s.y - f.y) / L
            l -= 1
        result.append(Point(f.x * 30 - 5, -f.y * 30 - 5))
        result.append(Point(s.x * 30 - 5, -s.y * 30 - 5))
        draw(result)

    def bresenham(self):
        points = []
        x1, y1 = self.x1, self.y1
        x2, y2 = self.x2, self.y2
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append(Point(x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        draw(points)


    def bre_method_circle(self):
        res = []
        x = floor(self.x)
        y = floor(self.y)
        r = self.r
        newx = self.r
        newy = 0
        t1 = r // 16
        while newx >= newy:
            symmetric_add(newx, newy, x, y, res)
            newy += 1
            t1 += newy
            t2 = t1 - newx
            if t2 >= 0:
                t1 = t2
                newx -= 1
        draw(res)

    def on_enter1(self, text):
        self.x1 = int(text)

    def on_enter2(self, text):
        self.y1 = int(text)

    def on_enter3(self, text):
        self.x2 = int(text)

    def on_enter4(self, text):
        self.y2 = int(text)

    def on_enter5(self, text):
        self.r = int(text)


class Editor(App):
    pass


Factory.register('Root', cls=Root)

if __name__ == '__main__':
    Editor().run()
