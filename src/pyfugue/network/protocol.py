# -*- coding: utf-8 -*-
from twisted.conch import telnet
from twisted.logger import Logger
from twisted.protocols import basic

from . import options


__log__ = Logger()


class MUDProtocol(basic.LineReceiver, telnet.TelnetProtocol):
    delimiter = b"\n"

    def __init__(self):
        self.options = {}
        for option in [
            options.EOR,
            options.NAWS,
            options.STARTTLS,
            options.MSSP,
            options.ZMP,
            options.TTYPE,
            options.MSDP,
            options.GMCP,
            options.TIMING_MARK,
        ]:
            self.options[option.code] = option(self)

    def _debug(self, *args):
        __log__.debug(repr(args))

    def lineReceived(self, data):
        self.factory.controller.received(data)

    #        self.factory.controller.applicationDataReceived(data)

    def dataReceived(self, data):
        super().dataReceived(data)
        if self._buffer:
            self._debug("PROMPT:", self._buffer)

    def unhandledCommand(self, command, argument):
        __log__.debug(repr(("command", command, argument)))

    def unhandledSubnegotiation(self, command, data):
        self._debug("subnegotiation", command, data)

    def __enable(self, option, local):
        item = self.options.get(option, None)
        name = item.name if item else "unknown"
        __log__.debug(
            repr(("enableLocal" if local else "enableRemote", ord(option), name))
        )
        if item:
            if local:
                return item.enableLocal()
            else:
                return item.enableRemote()
        else:
            return False

    def enableLocal(self, option):
        return self.__enable(option, local=True)

    def enableRemote(self, option):
        return self.__enable(option, local=False)

    def __disable(self, option, local):
        __log__.debug(repr(("disableLocal" if local else "disableRemote", option)))
        if option in self.options:
            item = self.options[option]
            if local:
                return item.disableLocal()
            else:
                return item.disableRemote()
        else:
            raise NotImplementedError(
                "Don't know how to disable {} telnet option {!r}".format(
                    "local" if local else "remote", option
                )
            )

    def disableLocal(self, option):
        return self.__disable(option, local=True)

    def disableRemote(self, option):
        return self.__disable(option, local=False)

    def __getattr__(self, name):
        for _, option in self.option.items():
            if name == option.__class__.__name__:
                return option
        raise AttributeError
