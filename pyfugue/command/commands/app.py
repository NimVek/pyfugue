# -*- coding: utf-8 -*-
import logging

from . import command


__log__ = logging.getLogger(__name__)


class Quit(command.OptionCommand):
    def __init__(self):
        super().__init__()

    def _execute(self, session, args):
        __log__.debug(repr(args))
        session.app.stop()
