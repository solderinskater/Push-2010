#!/usr/bin/python
import bluetooth
import serial

bd_addr = "00:06:66:02:F1:FC"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

print "Connected: ", bd_addr

while 1:
    line = sock.recv(1024);
    print line

sock.close()
