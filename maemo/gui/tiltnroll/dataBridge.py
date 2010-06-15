# Copyright 2010 Keywan Tonekaboni, Florian Fusco, Stefanie Schirmer, Alexander Lenhard, Erik Weitnauer <eweitnauer at gmail.com>
#
# This file is part of Soldering Skaters Nokia Push Project.
#
# Soldering Skaters Nokia Push Project is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Soldering Skaters Nokia Push Project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Soldering Skaters Nokia Push Project.  If not, see <http://www.gnu.org/licenses/>.
_all_=['Board','DataBridge']


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
#            retcode = subprocess.call("rfcomm connect rfcomm0 00:06:66:02:F1:FC &", shell=True)
            retcode = subprocess.call("rfcomm connect rfcomm0 00:06:66:02:F1:FE &", shell=True)
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
   #     self.data = self.data1.strip() + self.data2
        return self.data
    
    def stop(self):
        self.ser1.close()
#        self.ser2.close()


