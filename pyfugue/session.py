# -*- coding: utf-8 -*-
from twisted.internet import reactor
from twisted.logger import Logger

from . import network

__log__ = Logger()


class Session:
    def __init__(self, app):
        self.app = app
        self.ui = self.app.ui.create_session(self)
        self.connection = None

    @property
    def connected(self):
        return (
            self.connection
            and self.connection.protocol
            and self.connection.protocol.transport
        )

    def activate(self):
        pass

    def connect(self, host, port):
        factory = network.MUDClientFactory(self)
        reactor.connectTCP(host, port, factory)
        pass

    def commit(self, text):
        if text.startswith("/"):
            self.app.command(self, text[1:])
        else:
            if not self.connected:
                __log__.warn("Not Connected")
            else:
                self.connection.protocol.transport.write((text + "\r\n").encode())
                # sending
                pass

    #    def hook(self,
    def received(self, line):
        self.ui.display(line)
