# -*- coding: utf-8 -*-
class Option:

    code = bytes()

    def __init__(self, protocol):
        self.protocol = protocol

    @property
    def name(self):
        return self.__class__.__name__

    def local(self):
        self.protocol.transport.getOptionState(self.code).us.state == "yes"

    def remote(self):
        self.protocol.transport.getOptionState(self.code).him.state == "yes"

    def enableLocal(self):
        return False

    def enableRemote(self):
        return False

    def disableLocal(self):
        raise NotImplementedError(
            f"Don't know how to disable local telnet option {self.code!r}"
        )

    def disableRemote(self):
        raise NotImplementedError(
            f"Don't know how to disable remote telnet option {self.code!r}"
        )

    def requestNegotiation(self, data):
        return self.protocol.transport.requestNegotiation(self.code, data)

    def negotiate(self, data):
        pass

    def decode(self, data):
        return data.decode("iso-8859-1")

    def encode(self, data):
        return data.encode("iso-8859-1")
