#!/usr/bin/env python

usage = """Usage:
python example-signal-emitter.py &
python example-signal-recipient.py
python example-signal-recipient.py --exit-service
"""

import sys
import traceback

import gobject

import dbus
import dbus.mainloop.glib

def handle_reply(msg):
    print msg

def handle_error(e):
    print str(e)



def hello_signal_handler(hello_string):
    print ("Received signal (by connecting using remote object) and it says: "
           + str(hello_string))

def catchall_signal_handler(*args, **kwargs):
    print ("Caught signal (in catchall handler) "
           + kwargs['dbus_interface'] + "." + kwargs['member'])
    for arg in args:
        print "        " + str(arg)

def catchall_shout_signals_handler(hello_string):
    for item in hello_string:
        print "* shout " + str(item)
    print "----" 

def catchall_level_signals_handler(hello_string):
    print "# level " + str(hello_string)

def catchall_music_signals_handler(hello_string):
    print "+ music " + str(hello_string)
    
def catchall_testservice_interface_handler(hello_string, dbus_message):
    for item in hello_string:
        print "voila " + str(item)
    #print "net.prometoys.solderinskater.TrickService interface says '" + str(hello_string) + "' when it sent signal " + dbus_message.get_member()


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.bus.BusConnection('tcp:host=localhost,port=1337')
    try:
        object  = bus.get_object("net.prometoys.solderinskater.TrickService","/net/prometoys/solderinskater/TrickService/DbusTrickObject")

#        object.connect_to_signal("ShoutSignal", hello_signal_handler, dbus_interface="net.prometoys.solderinskater.TrickService", arg0="Hello")
    except dbus.DBusException:
        traceback.print_exc()
        print usage
        sys.exit(1)

    bus.add_signal_receiver(catchall_shout_signals_handler, dbus_interface = "net.prometoys.solderinskater.TrickService", signal_name = "ShoutSignal")

    bus.add_signal_receiver(catchall_level_signals_handler, dbus_interface = "net.prometoys.solderinskater.TrickService", signal_name = "LevelSignal")


    loop = gobject.MainLoop()
    loop.run()
