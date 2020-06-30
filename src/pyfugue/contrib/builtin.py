from enum import Enum


__all__ = ["AutoName"]


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
