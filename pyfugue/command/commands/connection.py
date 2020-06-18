# -*- coding: utf-8 -*-
import logging

from . import command


__log__ = logging.getLogger(__name__)


class Connect(command.OptionCommand):
    def __init__(self):
        super().__init__()
        self.parser.add_argument("hostname")
        self.parser.add_argument("port", nargs="?", type=int, default=23)

    def _execute(self, session, args):
        __log__.debug(repr(args))
        session.connect(args.hostname, args.port)
