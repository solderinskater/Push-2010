# test some stuff on the bus

require 'rubygems'
require 'dbus_client' # http://github.com/pangdudu/dbus-client
#require 'unprof'
include DBusClient

dbus = DBus::RemoteBus.new("tcp:host=0.0.0.0,port=1337")
#try client lib
list_names dbus
#get a proxy object
service_name = "org.sskaters.Sensors"
obj_path = "/org/sskaters/Sensors/Gyroscope"
default_iface = "org.sskaters.Sensors.Interface"
gyro = get_object_from_service dbus,service_name,obj_path,default_iface
#call a method on the proxy object
gyro.poll_sensor
