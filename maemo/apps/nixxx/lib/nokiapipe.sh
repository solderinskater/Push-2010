#!/bin/sh
gst-launch-0.10 filesrc location=../sounds/startup.mp3 ! mp3parse ! nokiamp3dec ! audioconvert ! pulsesink
