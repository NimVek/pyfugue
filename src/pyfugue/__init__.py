# -*- coding: utf-8 -*-
from ._version import __version__
from .application import Application


__title__ = "pyfugue"


def main():
    Application().start()
