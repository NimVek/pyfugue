# -*- coding: utf-8 -*-
from twisted import logger
from twisted.internet import ssl
from twisted.python.compat import _bytesChr as chr

from . import option


__log__ = logger.Logger()

__all__ = ["STARTTLS"]


FOLLOWS = chr(1)


class STARTTLS(option.Option):
    code = chr(46)

    def enableLocal(self):
        self.protocol.transport.negotiationMap[self.code] = self.negotiate
        return True

    def negotiate(self, data):
        __log__.debug(repr(data))
        __log__.debug(repr(FOLLOWS))
        __log__.debug(repr(b"".join(data) == FOLLOWS))
        self.requestNegotiation(FOLLOWS)
        self.protocol.transport.startTLS(ssl.CertificateOptions(verify=False))


#    def size(self, width, height):
#        self.requestNegotiation(struct.pack('!HH', width, height))
