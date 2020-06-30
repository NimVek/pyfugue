from enum import auto

from pyfugue.contrib.builtin import AutoName


class Hooks(AutoName):
    DISPLAY = auto()


MAX = float("inf")
STANDARD = 1
MIN = float("-inf")
DEFAULT = MIN
