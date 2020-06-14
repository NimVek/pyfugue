# -*- coding: utf-8 -*-
import pprint

import gi
from gi.repository import Gtk

gi.require_version('Gtk', '3.0')

__all__ = ['UI']


class SessionWindow:

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('pyfugue.ui')
        self.builder.connect_signals(self)

        self.output = self.builder.get_object('output').get_buffer()
        self.output.create_mark('end', self.output.get_end_iter())
        self.outputwin = self.builder.get_object('output')
        self.window = self.builder.get_object('window')
        self.window.show_all()

    def on_input_activate(self, entry):
        line = entry.get_text()
        entry.set_text('')
        end = self.output.get_mark('end')
        self.output.insert(self.output.get_iter_at_mark(end), line + '\n')
        self.outputwin.scroll_mark_onscreen(end)

    def on_window_destroy(self, _):
        pass


class Application(Gtk.Application):
    def do_activate(self):
        self.window = SessionWindow()


class UI:
    def __init__(self):
        from twisted.internet import gtk3reactor
        gtk3reactor.install()

    def startup(self):
        from twisted.internet import reactor
        app = Application()
        reactor.registerGApplication(app)
        reactor.run()
