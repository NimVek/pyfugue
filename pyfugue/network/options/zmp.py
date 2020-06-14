# -*- coding: utf-8 -*-
import datetime

from twisted import logger
from twisted.python.compat import _bytesChr as chr

from . import option

__log__ = logger.Logger()

__all__ = ["ZMP"]


NUL = chr(0)


class ZMP(option.Option):
    code = chr(93)

    def __init__(self, protocol):
        super().__init__(protocol)
        self.callbacks = {"zmp.ping": self.__ping, "zmp.check": self.__check}

    def enableRemote(self):
        self.protocol.transport.negotiationMap[self.code] = self.__negotiate
        return True

    def __negotiate(self, data):
        data = list(map(self.decode, b"".join(data).split(NUL)))
        cmd = data[0]
        args = data[1:-1]
        __log__.debug(repr([cmd, args]))
        if cmd == "zmp.check":
            self.send("zmp.support", *args)

    def ping(self):
        self.send("zmp.ping")

    def __ping(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        self.send("zmp.time", now.isoformat(sep=" ", timespec="seconds"))

    def __check(self, package):
        self.send("zmp.support", package)

    def input(self, line):
        self.send("zmp.input", package)

    def send(self, command, *args):
        data = NUL.join(map(self.encode, [command, *args])) + NUL
        __log__.debug(repr(data))
        self.requestNegotiation(data)
