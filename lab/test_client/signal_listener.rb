# test some stuff on the bus

require 'rubygems'
require 'dbus'
require 'dbus_client' # http://github.com/pangdudu/dbus-client
#require 'unprof'
include DBusClient

dbus = DBus::RemoteBus.new("tcp:host=0.0.0.0,port=1337")
#dbus = DBus::SessionBus.instance
#subscribe on newData signals
mr = DBus::MatchRule.new
mr.type = "signal"
mr.interface = "org.sskaters.Sensors.Interface"
mr.path = "/org/sskaters/Sensors/Gyroscope"
dbus.add_match(mr) { |data| dlog "incoming data: #{data.params.inspect}" }
#and go into dbus main loop
Thread.new { dbus_main dbus }
loop { sleep 1 }
