import enum


class Hook(enum.Enum):
    SEND = enum.auto()
    PROMPT = enum.auto()
    ATCP = enum.auto()
    GMCP = enum.auto()
