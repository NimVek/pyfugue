# -*- coding: utf-8 -*-
from twisted.internet import protocol

from .protocol import MUDProtocol
from .transport import MUDTransport


class MUDClientFactory(protocol.ClientFactory):

    #    protocol = MUDProtocol
    #    protocol = MUDTransport
    #    protocol = lambda x: MUDTransport(MUDProtocol)

    def __init__(self, controller):
        self.controller = controller

    def buildProtocol(self, addr):
        self.transport = MUDTransport(MUDProtocol)
        self.transport.factory = self
        self.controller.connection = self.transport
        return self.transport
