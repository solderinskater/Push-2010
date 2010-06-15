#simplest ruby program to read from arduino serial, 
#using Ruby/SerialPort library
#(http://ruby-serialport.rubyforge.org)
require 'rubygems'
require 'serialport'

=begin
begin
  Kernel::require "serialport"
rescue
  puts "ERROR: requires ruby-serialport, available as a ruby gem"
  exit
end
=end

#params for serial port
port_str = "/dev/ttyUSB0"  #may be different for you
baud_rate = 115200 #9600
data_bits = 8
stop_bits = 1
parity = SerialPort::NONE

sp = SerialPort.new(port_str, baud_rate, data_bits, stop_bits, parity)

#just read forever
while true do
  printf("%c", sp.getc)
  puts Time.now
  sp.putc Time.now.to_s
end

sp.close 

