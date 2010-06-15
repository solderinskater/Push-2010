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

require 'dbus'
require 'dbus_client'
require 'rofl'
include DBusClient
include Rofl

dbus = DBus::RemoteBus.new('tcp:host=localhost,port=1337')
#subscribe on newData signals
mr = DBus::MatchRule.new
mr.type = "signal"

mr.interface = "net.prometoys.solderinskater.TrickService"
mr.path = "/net/prometoys/solderinskater/TrickService/DbusTrickObject"

dbus.add_match(mr) { |data| dlog "incoming data: #{data.params.inspect}" }
#and go into dbus main loop
dbus_main dbus
