# -*- coding: utf-8 -*-
import argparse


class Command:
    @property
    def name(self):
        return self.__class__.__name__.lower()

    def execute(self, session, *args):
        raise NotImplementedError


class OptionCommand(Command):
    def __init__(self):
        super().__init__()
        self.parser = argparse.ArgumentParser(prog=f"/{self.name}")

    def execute(self, session, *args):
        try:
            args = self.parser.parse_args(args)  # type: ignore
        except SystemExit:
            pass
        else:
            self._execute(session, args)

    def _execute(self, session, args):
        raise NotImplementedError
