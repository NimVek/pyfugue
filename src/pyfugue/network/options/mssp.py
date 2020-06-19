# -*- coding: utf-8 -*-
import datetime

from twisted import logger
from twisted.python.compat import _bytesChr as chr

from . import option


__log__ = logger.Logger()

__all__ = ["MSSP"]


CONVERTER = {
    # Required
    "PLAYERS": int,
    "UPTIME": lambda x: datetime.datetime.fromtimestamp(int(x)),
    # Generic
    "CRAWL DELAY": int,
    #        'PORT': int,
    "CREATED": int,
    # Protocols
    "ANSI": lambda x: bool(int(x)),
    "GMCP": lambda x: bool(int(x)),
    "MCCP": lambda x: bool(int(x)),
    "MCP": lambda x: bool(int(x)),
    "MSDP": lambda x: bool(int(x)),
    "MSP": lambda x: bool(int(x)),
    "MXP": lambda x: bool(int(x)),
    "PUEBLO": lambda x: bool(int(x)),
    "ZMP": lambda x: bool(int(x)),
    "UTF-8": lambda x: bool(int(x)),
    "VT100": lambda x: bool(int(x)),
    "XTERM 256 COLORS": lambda x: bool(int(x)),
    "XTERM TRUE COLORS": lambda x: bool(int(x)),
    # Commercial
    "PAY TO PLAY": lambda x: bool(int(x)),
    "PAY FOR PERKS": lambda x: bool(int(x)),
    # Hiring
    "HIRING BUILDERS": lambda x: bool(int(x)),
    "HIRING CODERS": lambda x: bool(int(x)),
}


VAR = chr(1)
VAL = chr(2)


class MSSP(option.Option):
    code = chr(70)

    def enableRemote(self):
        self.protocol.transport.negotiationMap[self.code] = self.negotiate
        return True

    def negotiate(self, data):
        self.values = {}
        data = b"".join(data)
        for var in data.split(VAR)[1:]:
            val = list(map(self.decode, var.split(VAL)))
            key = val[0]
            if key in CONVERTER:
                val = list(map(CONVERTER[key], val[1:]))
            else:
                val = val[1:]
            if len(val) == 1:
                val = val[0]
            self.values[key] = val
        __log__.debug(self.values)
