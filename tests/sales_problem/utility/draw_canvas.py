# -*- coding: utf-8 -*-

import tkinter


class DisplayCanvas:
    def __init__(self, root, width, height):
        self._canvas = tkinter.Canvas(root, width=width, height=height, bg="white")
        self._canvas.pack()

    def draw_path(self, path):
        self._canvas.delete("line")
        x0, y0 = path[0]
        for i in range(1, len(path)):
            x1, y1 = path[i]
            self._canvas.create_line(x0, y0, x1, y1, tag="line")
            x0, y0 = x1, y1
        self._canvas.create_line(x0, y0, path[0][0], path[0][1], tag="line")
        self._canvas.update()

    def draw_point(self, path):
        for x, y in path:
            self._canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill ="green")
