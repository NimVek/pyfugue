# -*- coding: utf-8 -*-
import telnetlib

from twisted import logger
from twisted.internet import reactor, ssl
from twisted.python.compat import _bytesChr as chr

from . import option


__log__ = logger.Logger()

__all__ = ["STARTTLS"]


FOLLOWS = chr(1)


class STARTTLS(option.Option):
    code = telnetlib.TLS

    def enableLocal(self):
        self.protocol.transport.negotiationMap[self.code] = self.negotiate
        return True

    def negotiate(self, data):
        assert b"".join(data) == FOLLOWS
        self.requestNegotiation(FOLLOWS)
        reactor.callLater(1, self._starttls)

    def _starttls(self):
        self.protocol.transport.startTLS(ssl.CertificateOptions(verify=False))
