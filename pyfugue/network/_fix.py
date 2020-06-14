# -*- coding: utf-8 -*-
from twisted.conch import telnet
from twisted.python.compat import iterbytes


class TelnetTransport(telnet.TelnetTransport):
    """
    Fix for diffrent telnet commands
    """

    def dataReceived(self, data):
        appDataBuffer = []

        for b in iterbytes(data):
            if self.state == 'data':
                if b == telnet.IAC:
                    self.state = 'escaped'
                elif b == b'\r':
                    self.state = 'newline'
                else:
                    appDataBuffer.append(b)
            elif self.state == 'escaped':
                if b == telnet.IAC:
                    appDataBuffer.append(b)
                    self.state = 'data'
                elif b == telnet.SB:
                    self.state = 'subnegotiation'
                    self.commands = []
                elif b in (telnet.WILL, telnet.WONT, telnet.DO, telnet.DONT):
                    self.state = 'command'
                    self.command = b
                else:
                    self.state = 'data'
                    if appDataBuffer:
                        self.applicationDataReceived(b''.join(appDataBuffer))
                        del appDataBuffer[:]
                    self.commandReceived(b, None)
            elif self.state == 'command':
                self.state = 'data'
                command = self.command
                del self.command
                if appDataBuffer:
                    self.applicationDataReceived(b''.join(appDataBuffer))
                    del appDataBuffer[:]
                self.commandReceived(command, b)
            elif self.state == 'newline':
                self.state = 'data'
                if b == b'\n':
                    appDataBuffer.append(b'\n')
                elif b == b'\0':
                    appDataBuffer.append(b'\r')
                elif b == telnet.IAC:
                    # IAC isn't really allowed after \r, according to the
                    # RFC, but handling it this way is less surprising than
                    # delivering the IAC to the app as application data.
                    # The purpose of the restriction is to allow terminals
                    # to unambiguously interpret the behavior of the CR
                    # after reading only one more byte.  CR LF is supposed
                    # to mean one thing (cursor to next line, first column),
                    # CR NUL another (cursor to first column).  Absent the
                    # NUL, it still makes sense to interpret this as CR and
                    # then apply all the usual interpretation to the IAC.
                    appDataBuffer.append(b'\r')
                    self.state = 'escaped'
                else:
                    appDataBuffer.append(b'\r' + b)
            elif self.state == 'subnegotiation':
                if b == telnet.IAC:
                    self.state = 'subnegotiation-escaped'
                else:
                    self.commands.append(b)
            elif self.state == 'subnegotiation-escaped':
                if b == telnet.SE:
                    self.state = 'data'
                    commands = self.commands
                    del self.commands
                    if appDataBuffer:
                        self.applicationDataReceived(b''.join(appDataBuffer))
                        del appDataBuffer[:]
                    self.negotiate(commands)
                else:
                    self.state = 'subnegotiation'
                    self.commands.append(b)
            else:
                raise ValueError("How'd you do this?")

        if appDataBuffer:
            self.applicationDataReceived(b''.join(appDataBuffer))
