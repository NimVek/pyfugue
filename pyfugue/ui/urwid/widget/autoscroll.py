# -*- coding: utf-8 -*-
import urwid

from ..tools import ISignal


class AutoScroll(urwid.WidgetWrap, ISignal):
    signals = ["size"]

    def __init__(self):
        self.__lines = urwid.SimpleListWalker([])
        self.__display = urwid.ListBox(self.__lines)
        self.__size = None
        self.autoscroll = True
        super().__init__(urwid.Frame(self.__display))

    def append(self, text):
        self.__lines.append(text)
        if self.autoscroll:
            self.__display.set_focus(len(self.__lines) - 1)

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        if not self.size or value[0] != self.size[0] or value[1] != self.size[1]:
            self.__size = value
            self.emit_signal("size", *value)

    def render(self, size, focus=False):
        canvas = super().render(size, focus)
        self.size = (canvas.cols(), canvas.rows())
        return canvas

    def keypress(self, size, key):
        result = super().keypress(size, key)
        if not result:
            if key in ["up", "page up"]:
                self.autoscroll = False
            elif key in ["down", "page down"]:
                self.autoscroll = self.__display.focus_position == len(self.__lines) - 1
