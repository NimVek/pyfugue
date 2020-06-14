# -*- coding: utf-8 -*-
import urwid

from . import widget


class UISession(urwid.Frame):

    def __init__(self, ui, session):
        self.ui = ui
        self.session = session
        self.__output = widget.AutoScroll()
        self.__status = urwid.Divider('_')
        self.__input = widget.Readline()
        self.__grid = widget.Grid()
        self.__log = urwid.WidgetWrap(urwid.WidgetDisable(None))
        overlay = urwid.WidgetDisable(urwid.Pile([self.__log, self.__grid]))
        display = urwid.Overlay(overlay, self.__output, urwid.CENTER,
                                urwid.RELATIVE_100, urwid.BOTTOM, urwid.PACK)
        super().__init__(display,
                         footer=urwid.Pile([self.__status, self.__input], focus_item=1), focus_part='footer')
        self.prompt = '> '
        self.__input.connect_signal('commit', self.on_commit)

    @property
    def size(self):
        return self.__output.size

    @property
    def input(self):
        return self.__input.edit_text

    @input.setter
    def input(self, text):
        self.__input.edit_text = text

    @property
    def prompt(self):
        return self.__input.caption.text

    @prompt.setter
    def prompt(self, text):
        self.__input.set_caption((urwid.AttrSpec('bold', 'default'), text))

    @property
    def log(self):
        return self.__log._w

    @log.setter
    def log(self, log):
        self.__log._w = log

    def display(self, text):
        self.__output.append(urwid.Text(text))
        self.ui.loop.draw_screen()

    def on_commit(self, widget, text):
        text = text.strip()
        if text:
            self.session.commit(text)

    def keypress(self, size, key):
        if key in ['page up', 'page down', 'shift up', 'shift down']:
            if key.startswith('shift '):
                key = key[6:]
            result = self.__output.keypress(size, key)
        else:
            (columns, _) = size
            result = self.__input.keypress((columns,), key)
        if result:
            self.display(repr(('unhandled', result)))
        return result
