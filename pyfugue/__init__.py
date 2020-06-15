# -*- coding: utf-8 -*-
from .application import Application
from ._version import __version__

__title__ = "pyfugue"


def main():
    Application().start()
