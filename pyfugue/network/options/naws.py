# -*- coding: utf-8 -*-
import struct

from twisted.conch import telnet

from . import option


class NAWS(option.Option):
    code = telnet.NAWS

    def enableLocal(self):
        return True

    def size(self, width, height):
        self.requestNegotiation(struct.pack('!HH', width, height))
