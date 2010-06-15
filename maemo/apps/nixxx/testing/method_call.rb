# Copyright 2010 Nick Thomas <pangdudu at gmail.com>
# This file is part of the Soldering Skaters Nokia Push Project
# (short: the project).
# 
# The project is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# The project is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with the project.  If not, see <http://www.gnu.org/licenses/>.

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
