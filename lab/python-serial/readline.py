#!/usr/bin/python
import serial

ser = serial.Serial('/dev/rfcomm0', 115200, timeout=1)
while 1:
    line = ser.readline()   # read a '\n' terminated line
    print line
ser.close()
