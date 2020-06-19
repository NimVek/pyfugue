# -*- coding: utf-8 -*-
from functools import partial

import urwid


class ISignal:
    def emit_signal(self, name, *arguments):
        urwid.signals.emit_signal(self, name, self, *arguments)

    def __forward_signal(self, name, obj, *arguments):
        urwid.signals.emit_signal(self, name, obj, *arguments)

    def forward_signal(self, obj, name):
        urwid.signals.connect_signal(obj, name, partial(self.__forward_signal, name))

    def connect_signal(self, name, callback):
        urwid.signals.connect_signal(self, name, callback)


class Signal(ISignal, metaclass=urwid.signals.MetaSignals):
    pass
