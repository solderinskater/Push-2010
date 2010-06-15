_all_=['Board','DataBridge']


import bluetooth
import serial
import subprocess
import time
from os import *
import sys

class Board:
    def __init__(self):
        target_prefix = "Diptera"
        target_address = None
        self.addr=[]
        self.sock = None

#        nearby_devices = bluetooth.discover_devices()
#        print nearby_devices

#        for bdaddr in nearby_devices:
##            device_name = bluetooth.lookup_name( bdaddr )
#            if device_name is not None:
#                if device_name.startswith(target_prefix):
#                    print "Found Diptera bluetooth device ", device_name, bdaddr
#                    self.addr.append(bdaddr)

    def connect(self, boardNumber):
        port = 1

#        if self.sock!=None:
#            self.sock.close()
#        self.sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
#        self.sock.connect((self.addr[boardNumber], port))
#        subprocess.Popen('/usr/bin/rfcomm connect rfcomm0 ' + str(self.addr[boardNumber]) + '&', shell=True)
#        os.system('rfcomm connect rfcomm0 00:06:66:02:F1:FC')
        try:
            retcode = subprocess.call("rfcomm connect rfcomm0 00:06:66:02:F1:FC &", shell=True)
            if retcode < 0:
                print >>sys.stderr, "Child was terminated by signal", -retcode
            else:
                print >>sys.stderr, "Child returned", retcode
        except OSError, e:
            print >>sys.stderr, "Execution failed:", e

class DataBridge:
    def __init__(self):
        self.board = Board()

    def start(self):
        self.board.connect(0)
        con = False
        i=1
        while not con:
            try:
                self.ser1 = serial.Serial('/dev/rfcomm0', 115200, timeout=1)
                con=True
            except:
                con=False
                print "Try "+str(i)
                i=i+1
                time.sleep(2)

                
        return con
        #        self.board.connect(1)
         #       self.ser2 = serial.Serial('/dev/rfcomm1', 115200, timeout=1)

    def readline(self):
        self.data = self.ser1.readline()
  #      self.data2 = self.ser2.readline()
   #     self.data = string.join(string.split(self.data1,',').append(self.data2,','),',')
        return self.data
    
    def stop(self):
        self.ser1.close()
        self.ser2.close()


