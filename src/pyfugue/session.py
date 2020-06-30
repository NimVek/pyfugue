# -*- coding: utf-8 -*-
from typing import Any

from twisted.internet import reactor
from twisted.logger import Logger

from . import network
from .contrib import messaging
from .tools.hook import Hooks


__log__ = Logger()


class Session(messaging.Publisher):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.ui = self.app.ui.create_session(self)
        self.connection = None  # type: Any

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

    def commit(self, text):
        if text.startswith("/"):
            self.app.command(self, text[1:])
        else:
            if not self.connected:
                __log__.warn("Not Connected")
            else:
                self.connection.protocol.transport.write((text + "\r\n").encode())

    def received(self, line):
        self.publish(messaging.Message(Hooks.DISPLAY, line))
