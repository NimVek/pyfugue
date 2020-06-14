# -*- coding: utf-8 -*-
from twisted.conch import telnet

from . import _fix


class MUDTransport(_fix.TelnetTransport):

    def __init__(self, protocolFactory=None, *a, **kw):
        super().__init__(protocolFactory, *a, **kw)
        self.__busy = False
        self.__buffer = b''

    def dataReceived(self, data):
        if self.__busy:
            self.__buffer += data
            return

        try:
            self.__busy = True
            self.__buffer += data
            while self.__buffer:
                before, separator, self.__buffer = self.__buffer.partition(
                    telnet.IAC + telnet.SE)
                if not separator and before.endswith(telnet.IAC):
                    self.__buffer = telnet.IAC + self.__buffer
                    before = before[:-1]
                super().dataReceived(before + separator)
                if not separator:
                    break
        finally:
            self.__busy = False

    def startTLS(self, contextFactory):
        self.options = {}
        self.transport.startTLS(contextFactory)
