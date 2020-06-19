# -*- coding: utf-8 -*-
from twisted.logger import Logger

from . import command, session, ui


__log__ = Logger()


class Application:
    def start(self):
        self.ui = ui.UIController()
        self.active = session.Session(self)
        self.commands = command.Controller()
        self.ui.start()

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, session):
        self.__active = session
        self.ui.active = session.ui

    def stop(self):
        self.ui.stop()

    def command(self, session, command):
        __log__.debug(repr(("command", session, command)))
        self.commands.execute(session, command)
