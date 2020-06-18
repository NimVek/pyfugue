# -*- coding: utf-8 -*-
import contextlib
import difflib
import logging
import re
import shlex

from . import commands


__log__ = logging.getLogger(__name__)


class StreamToLog:

    _buffer = ""
    _busy = False
    _separator = r"\r\n|\r|\n"

    def __init__(self, func):
        self._func = func

    def write(self, data):
        if self._busy:
            self._buffer += data
            return len(data)

        try:
            self._busy = True
            self._buffer += data
            while self._buffer:
                try:
                    part, self._buffer = re.split(
                        self._separator, self._buffer, maxsplit=1
                    )
                except ValueError:
                    return len(data)
                else:
                    self.forward(part)
        finally:
            self._busy = False

    def forward(self, part):
        self._func(part)


class Controller:
    def __init__(self):
        self.commands = {}
        self.__add_commands__(commands.Command)

    def __add_commands__(self, cls):
        subs = cls.__subclasses__()
        if not subs:
            self.add(cls())
        else:
            for i in subs:
                self.__add_commands__(i)

    def add(self, cmd):
        self.commands[cmd.name] = cmd

    def search(self, cmd):
        cmd = cmd.lower()
        if cmd in self.commands:
            return self.commands[cmd]
        else:
            result = [k for k in self.commands.keys() if k.startswith(cmd)]
            if len(result) == 1:
                return self.commands[result[0]]
            else:
                return result

    def execute(self, session, line):
        cmd, *args = shlex.split(line)
        command = self.search(cmd)
        if isinstance(command, commands.Command):
            with contextlib.redirect_stdout(
                StreamToLog(__log__.info)
            ), contextlib.redirect_stderr(StreamToLog(__log__.error)):
                command.execute(session, *args)
        else:
            if not command:
                command = difflib.get_close_matches(cmd, self.commands.keys())
            if command:
                __log__.warning(f"Command '/{cmd}' not found, did you mean:")
                __log__.warning("")
                for i in command:
                    __log__.warning(f"  command '/{i}'")
            else:
                __log__.error(f"/{cmd}: command not found")
