# -*- coding: utf-8 -*-
import enum
import telnetlib

import pyfugue
from twisted import logger
from twisted.python.compat import _bytesChr as chr

from . import option

__log__ = logger.Logger()

__all__ = ['TTYPE']


class MTTS(enum.Flag):
    ANSI = 1
    VT100 = 2
    UTF8 = 4
    COLORS256 = 8
    MOUSETRACKING = 16
    OSCCOLORPALETTE = 32
    SCREENREADER = 64
    PROXY = 128
    TRUECOLOR = 256
    MNES = 512


class State(enum.Enum):
    CLIENT = enum.auto()
    TERMINAL_TYPE = enum.auto()
    MTTS = enum.auto()


IS = chr(0)
SEND = chr(1)


class TTYPE(option.Option):
    code = telnetlib.TTYPE

    def enableLocal(self):
        self.state = State.CLIENT
        self.protocol.transport.negotiationMap[self.code] = self.negotiate
        return True

    def disableLocal(self):
        self.state = State.CLIENT
        self.protocol.transport.negotiationMap.pop(self.code, None)
        return True

    def negotiate(self, data):
        assert b''.join(data) == SEND
        if self.state == State.CLIENT:
            self.state = State.TERMINAL_TYPE
            self._is(pyfugue.__title__)
        elif self.state == State.TERMINAL_TYPE:
            self.state = State.MTTS
            self._is('ANSI')
        else:
            self._is('MTTS %d' % self.mtts.value)

    def _is(self, data):
        self.requestNegotiation(IS + (data.upper()).encode())

    @property
    def mtts(self):
        return MTTS.ANSI | MTTS.VT100 | MTTS.UTF8
