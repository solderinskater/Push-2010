#!/usr/bin/python

import commands
import serial,time

s = serial.Serial('/dev/ttyUSB0')

s.setDTR(0)
time.sleep(0.2)
s.setDTR(1)
time.sleep(0.2)
