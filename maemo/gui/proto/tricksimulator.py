_all_=["TrickSimulator"]
# -*- coding: UTF-8 -*-

import sys
import sip
import time
import dbus
from traceback import print_exc
import random
from dbus.mainloop.glib import DBusGMainLoop
import gobject

		
#iface.RaiseException(reply_handler=handle_raise_reply, 
#			  error_handler=handle_raise_error)
		
def replay():
	isStopped = False
	while not (isStopped):
		#print "and go"
		# Random warten
		sleeper = random.randint(1,2)
		trickno = random.randint(0,4)

		time.sleep(sleeper)
		
		iface.TrickCommit(tricks[trickno])
		print "hello dbus: " + tricks[trickno] + " after " + str(sleeper) 
		# iface.TrickCommit("Hello from Trick " + str(line))
	isStopped = True
		
def stop(self):
	isStopped = True
	print "WHEEEEEEEEEEEEEEEEEEEEEEEEEEEE\n\n\n"


tricks = ['ollie','360','kickflip','heelflip','shove']

#dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
#DBusGMainLoop(set_as_default=True)

isStopped = True
failed = False
hello_replied = False
raise_replied = False


bus = dbus.SessionBus()

try:
	remote_object = bus.get_object("net.prometoys.solderinskater.TrickService",
                                "/net/prometoys/solderinskater/TrickService/DbusTrickObject")

except dbus.DBusException:
	print_exc()
	sys.exit(1)

iface = dbus.Interface(remote_object, "net.prometoys.solderinskater.TrickService")

print "Tricksimulator ready to go"
replay()
