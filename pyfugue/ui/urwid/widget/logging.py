# -*- coding: utf-8 -*-
import datetime
import logging

import twisted.logger
import urwid


class LogEntry(urwid.WidgetWrap):
    def __init__(self, *args, **kwargs):
        self.__timestamp = datetime.datetime.now()
        super().__init__(*args, **kwargs)

    @property
    def timestamp(self):
        return self.__timestamp


class LogHandler(logging.Handler):
    color = {'CRITICAL': 'light red',
             'ERROR': 'dark red',
             'WARNING': 'yellow',
             'INFO': 'default',
             'DEBUG': 'dark magenta'}

    def __init__(self, target):
        super().__init__()
        self.setFormatter(logging.Formatter(fmt='% {message}', style='{'))
        self.__target = target

    def emit(self, record):
        msg = self.format(record)
        color = self.color.get(record.levelname, 'default')
        self.__target.append(urwid.Text(
            (urwid.AttrSpec(color, 'default'), msg)))


class LogObserver:
    color = {twisted.logger.LogLevel.critical: 'light red',
             twisted.logger.LogLevel.error: 'dark red',
             twisted.logger.LogLevel.warn: 'yellow',
             twisted.logger.LogLevel.info: 'default',
             twisted.logger.LogLevel.debug: 'dark magenta'}

    def __init__(self, target):
        self.__target = target

    def __call__(self, event):
        msg = twisted.logger.formatEvent(event)
        color = self.color.get(event['log_level'], 'default')
        self.__target.append(urwid.Text(
            (urwid.AttrSpec(color, 'default'), f'% {msg}')))


class Log(urwid.WidgetWrap):
    DURATION = 10

    def __init__(self, loop):
        self.__loop = loop
        self.log = urwid.Pile([])
        super().__init__(self.log)
        logging.basicConfig(format='%(filename)s:%(lineno)d:%(message)s',
                            level=logging.DEBUG, handlers=[LogHandler(self)])
        twisted.logger.globalLogPublisher.addObserver(LogObserver(self))

    def append(self, text):
        self.log.contents += [(LogEntry(text), (urwid.PACK, None))]
        self.log.set_focus(len(self.log.contents) - 1)
        self.cleanup(self.__loop)

    def cleanup(self, loop, user_data=None):
        threshold = datetime.datetime.now() - datetime.timedelta(seconds=self.DURATION)
        self.log.contents = [
            x for x in self._w.contents if x[0].timestamp > threshold]
        if self.log.contents:
            loop.set_alarm_in(self.DURATION // 2, self.cleanup)
