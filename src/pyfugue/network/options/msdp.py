# -*- coding: utf-8 -*-
from collections import abc

from twisted import logger
from twisted.internet import reactor
from twisted.python.compat import _bytesChr as chr

from . import option


__log__ = logger.Logger()

__all__ = ["MSDP"]


VAR = chr(1)
VAL = chr(2)
TABLE_OPEN = chr(3)
TABLE_CLOSE = chr(4)
ARRAY_OPEN = chr(5)
ARRAY_CLOSE = chr(6)


class MSDP(option.Option):
    code = chr(69)

    def enableRemote(self):
        self.protocol.transport.negotiationMap[self.code] = self.negotiate
        self.values = {}
        reactor.callLater(1, self._startup)
        return True

    def _encode_v(self, value):
        result = b""
        if isinstance(value, abc.Mapping):
            result = (
                TABLE_OPEN
                + b"".join([self._convert_kv(k, v) for k, v in value.items()])
                + TABLE_CLOSE
            )
        elif isinstance(value, abc.Sequence) and not isinstance(value, str):
            result = (
                ARRAY_OPEN + b"".join([self._convert_v(i) for i in value]) + ARRAY_CLOSE
            )
        else:
            result = str(value).encode()
        return VAL + result

    def _encode_kv(self, key, value):
        return VAR + str(key).encode() + self._encode_v(value)

    def _startup(self):
        self.requestNegotiation(self._encode_kv("LIST", "LISTS"))

    def _decode(self, data):
        result = len(data)
        for i in range(1, 7):
            tmp = data.find(i)
            if tmp != -1 and tmp < result:
                result = tmp
        return (data[:result].decode(), data[result:])

    def _decode_v(self, data):
        assert data[:1] == VAL
        if data[1:2] == TABLE_OPEN:
            data = data[2:]
            result = {}
            while data[:1] == VAR:
                (key, value, data) = self._decode_kv(data)
                result[key] = value
            assert data[:1] == TABLE_CLOSE
            return (result, data[1:])
        elif data[1:2] == ARRAY_OPEN:
            data = data[2:]
            result = []
            while data[:1] == VAL:
                (value, data) = self._decode_v(data)
                result.append(value)
            assert data[:1] == ARRAY_CLOSE
            return (result, data[1:])
        else:
            return self._decode(data[1:])

    def _decode_kv(self, data):
        assert data[:1] == VAR
        (key, data) = self._decode(data[1:])
        (value, data) = self._decode_v(data)
        return (key, value, data)

    def negotiate(self, data):
        (key, value, data) = self._decode_kv(b"".join(data))
        assert data == b""
        __log__.debug((self.name, key, value))
        if key not in self.values:
            if key == "LISTS":
                for i in value:
                    self.requestNegotiation(self._encode_kv("LIST", i))
        self.values[key] = value
