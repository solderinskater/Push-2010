#!/usr/bin/python2.5
# -*- coding: utf-8 -*-

import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk

class Main:
    def __init__(self):
        self.pipeline = gst.Pipeline("mypipeline")

        self.filesrc = gst.element_factory_make("filesrc", "source")
        self.pipeline.add(self.filesrc)
        self.filesrc.set_property("location", "music.mp3")

        self.decode = gst.element_factory_make("decodebin", "decode")
        self.decode.connect("new-decoded-pad", self.OnDynamicPad)
        self.pipeline.add(self.decode)

        self.filesrc.link(self.decode)

        self.convert = gst.element_factory_make("audioconvert", "convert")
        self.pipeline.add(self.convert)

        self.sink = gst.element_factory_make("pulsesink", "sink")
        self.pipeline.add(self.sink)

        self.convert.link(self.sink)

        self.pipeline.set_state(gst.STATE_PLAYING)

    def OnDynamicPad(self, dbin, pad, islast):
        print "OnDynamicPad Called!"
        pad.link(self.convert.get_pad("sink"))


start=Main()
gtk.main()

