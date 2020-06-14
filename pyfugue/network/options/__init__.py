# -*- coding: utf-8 -*-
import telnetlib

from . import option
from .msdp import MSDP
from .mssp import MSSP
from .naws import NAWS
from .starttls import STARTTLS
from .ttype import TTYPE
from .zmp import ZMP

__all__ = ["NAWS", "STARTTLS", "MSSP", "ZMP", "TTYPE", "MSDP", "EOR", "TIMING_MARK"]


class EOR(option.Option):
    code = telnetlib.EOR

    def enableRemote(self):
        return True


class TIMING_MARK(option.Option):
    code = telnetlib.TM

    def enableLocal(self):
        return True
