#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import urwid

from . import session, widget

__log__ = logging.getLogger(__name__)


class UIController:
    def __init__(self):
        self.__main = urwid.WidgetWrap(None)
        self.__loop = urwid.MainLoop(self.__main, event_loop=urwid.TwistedEventLoop())

        self.__log = widget.Log(self.loop)

    @property
    def active(self):
        return self.__main._w

    @active.setter
    def active(self, session):
        session.log = self.__log
        self.__main._w = session

    @property
    def loop(self):
        return self.__loop

    def start(self):
        self.__loop.run()

    def stop(self):
        __log__.debug("ui stop")
        raise urwid.ExitMainLoop()

    def create_session(self, controller):
        return session.UISession(self, controller)
