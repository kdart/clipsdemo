#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
#    Copyright (C) 2012- Keith Dart <keith@dartworks.biz>
#
#    This library is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    This library is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.

"""
Main App for CLIPS interaction and demo. There is an input area for evaluating
expressions, and multiple output areas corresponding to the varous "streams"
from CLIPS.

General purpose output indicators are also provided.


"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

import sys
import os
import time

import kivy
kivy.require("1.8.0")

import clips

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.codeinput import CodeInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from .lexer import JessLexer # At least close to clips syntax


def _now():
    return clips.Float(time.time())

class ClipsInput(CodeInput):
    def __init__(self, *args, **kwargs):
        super(ClipsInput, self).__init__(*args, **kwargs)
        self.lexer = JessLexer()
        self.hint_text = "Enter CLIPS code here."
        self.auto_indent = True
        self.background_color = (0.9, 1.0, 0.9, 1.)

    def _keyboard_on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[0] == 13 and modifiers == ['ctrl']:
            app = App.get_running_app()
            app.do_command()
            return
        super(ClipsInput, self)._keyboard_on_key_down(keyboard, keycode, text, modifiers)


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    text_input = ObjectProperty(None)

class ReadDialog(FloatLayout):
    read_input = ObjectProperty(None)


class ClipsDemoApp(App):

    def on_start(self):
        clips.RegisterPythonFunction(self._setstate1, "setstate1")
        clips.RegisterPythonFunction(self._getstate1, "getstate1")
        clips.RegisterPythonFunction(self._resetstate1, "resetstate1")
        clips.RegisterPythonFunction(self._setstate2, "setstate2")
        clips.RegisterPythonFunction(self._getstate2, "getstate2")
        clips.RegisterPythonFunction(self._resetstate2, "resetstate2")
        clips.RegisterPythonFunction(self._setstate3, "setstate3")
        clips.RegisterPythonFunction(self._getstate3, "getstate3")
        clips.RegisterPythonFunction(self._resetstate3, "resetstate3")
        clips.RegisterPythonFunction(self._setstate4, "setstate4")
        clips.RegisterPythonFunction(self._getstate4, "getstate4")
        clips.RegisterPythonFunction(_now, "now")
        #clips.RegisterPythonFunction(self.do_read, "read")

    def _setstate(self, num, args):
        lab = { 1: self.root.ids.state1,
                2: self.root.ids.state2,
                3: self.root.ids.state3,
                4: self.root.ids.state4,
                }[num]
        lab.color = (0.1, 0.9, 0.1, 1.)
        if args:
            lab.text = str(args[0])

    def _resetstate(self, num):
        lab = { 1: self.root.ids.state1,
                2: self.root.ids.state2,
                3: self.root.ids.state3,
                4: self.root.ids.state4,
                }[num]
        lab.color = (1, 1, 1, 1)
        lab.text = str("State{}".format(num))

    def _getstate(self, num):
        lab = { 1: self.root.ids.state1,
                2: self.root.ids.state2,
                3: self.root.ids.state3,
                4: self.root.ids.state4,
                }[num]
        return clips.String(str(lab.text))

    def _getstate1(self, *args):
        return self._getstate(1)

    def _getstate2(self, *args):
        return self._getstate(2)

    def _getstate3(self, *args):
        return self._getstate(3)

    def _getstate4(self, *args):
        return self._getstate(4)

    def _setstate1(self, *args):
        self._setstate(1, args)

    def _resetstate1(self, *args):
        self._resetstate(1)

    def _setstate2(self, *args):
        self._setstate(2, args)

    def _resetstate2(self, *args):
        self._resetstate(2)

    def _setstate3(self, *args):
        self._setstate(3, args)

    def _resetstate3(self, *args):
        self._resetstate(3)

    def _setstate4(self, *args):
        self._setstate(4, args)

    def _resetstate4(self, *args):
        self._resetstate(4)

    def do_command(self):
        self.command(self.root.ids.program.text)

    def do_eval(self):
        self.clipseval(self.root.ids.program.text)

    def do_run(self):
        try:
            clips.Run()
        except clips.ClipsError as err:
            self._update(error="ClipsError: {}".format(err))
            return
        self._update()

    def do_step(self):
        try:
            ran = clips.Run(1)
        except clips.ClipsError as err:
            self._update(error="ClipsError: {}".format(err))
            return
        self._update(trace="Ran {} rules.".format(ran))

    def do_reset(self):
        try:
            clips.Reset()
        except clips.ClipsError as err:
            self._update(error="ClipsError: {}".format(err))
            return
        self._update()
        for i in (1, 2, 3, 4):
            self._resetstate(i)

    def do_clear(self):
        try:
            clips.Clear()
        except clips.ClipsError as err:
            self._update(error="ClipsError: {}".format(err))
            return
        _buildfunctions()
        self._update()

    def command(self, text):
        try:
            clips.SendCommand(text, True)
        except clips.ClipsError as err:
            self._update(error="ClipsError: {}".format(err))
            return
        self._update()
        self.root.ids.program.text = ""

    def clipseval(self, text):
        try:
            rv = clips.Eval(text)
        except clips.ClipsError as err:
            self._update(error="ClipsError: {}".format(err))
            return
        self._update(trace="Eval: {}".format(rv))
        self.root.ids.program.text = ""

    def do_update(self):
        self._update()

    def _update(self, error="", warnings="", trace=""):
        ids = self.root.ids
        ids.stdout.text = _reader(clips.StdoutStream.Read)
        ids.display.text = _reader(clips.DisplayStream.Read)
        ids.trace.text = _reader(clips.TraceStream.Read) + trace
        ids.warnings.text = _reader(clips.WarningStream.Read) + warnings
        ids.errors.text = _reader(clips.ErrorStream.Read) + error

    def dismiss_popup(self):
        self._popup.dismiss()
        self._popup = None

    def do_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def do_save(self):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.dismiss_popup()
        try:
            clips.Load(filename[0])
        except clips.ClipsError as err:
            self._update(error="ClipsError: {}".format(err))
            return
        self._update()

    def save(self, path, filename):
        self.dismiss_popup()
        clips.Save(filename)
        self._update()

    def do_batch(self):
        content = LoadDialog(load=self.batch, cancel=self.dismiss_popup)
        self._popup = Popup(title="Run Batch", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def batch(self, path, filenames):
        self.dismiss_popup()
        for fname in filenames:
            try:
                clips.BatchStar(fname)
            except clips.ClipsError as err:
                self._update(error="ClipsError: {}".format(err))
                return
            self._update()

# TODO synchronous input (read function support)
#    def do_read(self):
#        content = ReadDialog()
#        self._popup = Popup(title="Read", content=content, size_hint=(0.9, 0.3))
#        self._popup.open()
#        try:
#            rv = self._read_input
#            print("XXX do_read", rv)
#            #return clips.String(rv)
#            self._update()
#            return rv
#        except:
#            ex, val, tb = sys.exc_info()
#            print("XXX Error", ex, val)
#            self.root.ids.errors.text = "Error: {}: {}".format(ex, val)
#            return None


def _reader(readmethod):
    out = readmethod()
    if out is None:
        return ""
    rv = []
    while out is not None:
        rv.append(out)
        out = readmethod()
    return "".join(rv)

def _buildfunctions():
    # simpler clips functions to set output indicators
    clips.BuildFunction("setstate1", "?text", '(python-call setstate1 ?text)')
    clips.BuildFunction("getstate1", None, '(python-call getstate1)')
    clips.BuildFunction("resetstate1", None, '(python-call resetstate1)')
    clips.BuildFunction("setstate2", "?text", '(python-call setstate2 ?text)')
    clips.BuildFunction("getstate2", None, '(python-call getstate2)')
    clips.BuildFunction("resetstate2", None, '(python-call resetstate2)')
    clips.BuildFunction("setstate3", "?text", '(python-call setstate3 ?text)')
    clips.BuildFunction("getstate3", None, '(python-call getstate3)')
    clips.BuildFunction("resetstate3", None, '(python-call resetstate3)')
    clips.BuildFunction("setstate4", "?text", '(python-call setstate4 ?text)')
    clips.BuildFunction("getstate4", None, '(python-call getstate4)')
    clips.BuildFunction("resetstate4", None, '(python-call resetstate4)')
    clips.BuildFunction("now", None, '(python-call now)')
    #clips.BuildFunction("read", None, '(python-call read)')

def main(argv):
    app = ClipsDemoApp()
    clips.SetExternalTraceback(True)
    _buildfunctions()
    if len(argv) > 1:
        try:
            clips.Load(argv[1])
        except clips.ClipsError as err:
            print (str(err))
            clips.Clear()
    clips.Reset()
    app.run()


if __name__ == "__main__":
    import sys
    main(sys.argv)

