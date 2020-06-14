# -*- coding: utf-8 -*-
import urwid

from ..tools import ISignal


class Readline(urwid.Edit, ISignal):
    signals = ['commit']

    def __init__(self):
        super().__init__(('bold', '> '))
        self.keymap = {
            'enter': self.commit
        }

    def commit(self):
        self.emit_signal('commit', self.edit_text)
        self.edit_text = ''

    def keypress(self, size, key):
        result = super().keypress(size, key)
        if result in self.keymap:
            self.keymap[result]()
            result = None
        return result
