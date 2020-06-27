# -*- coding: utf-8 -*-
from twisted import logger
from twisted.python.compat import _bytesChr as chr

from . import option


__log__ = logger.Logger()

__all__ = ["GMCP"]


class GMCP(option.Option):
    code = chr(201)

    def enableRemote(self):
        self.protocol.transport.negotiationMap[self.code] = self.negotiate
        return True

    def negotiate(self, data):
        __log__.debug(repr(data))
