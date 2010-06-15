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
_all_=["TrickSimulator"]
# -*- coding: UTF-8 -*-

import sys
import time
import dbus
from traceback import print_exc
import random
from dbus.mainloop.glib import DBusGMainLoop
import gobject

    
#iface.RaiseException(reply_handler=handle_raise_reply, 
#        error_handler=handle_raise_error)
    
def replay():
  isStopped = False
  while not (isStopped):
    #print "and go"
    # Random warten
    sleeper = random.randint(2,4)
    trickno = random.randint(0,1)
#    trickno = random.randint(0,9)

    time.sleep(sleeper)
    try:
      iface.TrickCommit(tricks[trickno])  
    except dbus.DBusException:
      print "tricksimulator: no dbus available, quit service"
      isStopped = True
    # iface.TrickCommit("Hello from Trick " + str(line))
  isStopped = True
    
def stop(self):
  isStopped = True

tricks = ['ollie','180']
#tricks = ['ollie','180','nollie360','nollie180','360','kickflip','heelflip','shove','frontsideflip','caballerial']

#dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
DBusGMainLoop(set_as_default=True)

isStopped = True
failed = False
hello_replied = False
raise_replied = False


#bus = dbus.SessionBus()
#bus = dbus.bus.BusConnection('tcp:host=localhost,port=1337')
bus = dbus.bus.BusConnection('unix:path=/tmp/skater_socket')

try:
  remote_object = bus.get_object("net.prometoys.solderinskater.TrickService",
                                 "/net/prometoys/solderinskater/TrickService/DbusTrickObject")

except dbus.DBusException:
  print "tricksimulator: FAIL: cant' find dbus. Abort"
  #print_exc()
  sys.exit(1)

iface = dbus.Interface(remote_object, "net.prometoys.solderinskater.TrickService")

replay()
