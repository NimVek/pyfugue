# -*- coding: utf-8 -*-
import math

import urwid


class Grid(urwid.WidgetWrap):
    def __init__(self):
        super().__init__(urwid.GridFlow([], 0, 1, 0, 'left'))
        self.__width = 0

    @property
    def width(self):
        return self.__width

    def __update_cell_width(self):
        result = 0
        if self._w.contents:
            item_count = len(self._w.contents)
            result = max([len(i[0].text) for i in self._w.contents])
            if self.width:
                tmp = self.width // (result+1)
                tmp = math.ceil(item_count/tmp)
                tmp = math.ceil(item_count/tmp)
                result = (self.width // tmp) - 1
        if self._w.cell_width != result:
            self._w.cell_width = result

    @property
    def contents(self):
        return self._w.contents

    @contents.setter
    def contents(self, contents):
        self._w.contents = contents
        self.__update_cell_width()

    def render(self, size, focus=False):
        canvas = super().render(size, focus)
        tmp = canvas.cols()
        if self.width != tmp:
            self.__width = tmp
            self.__update_cell_width()
        return canvas
