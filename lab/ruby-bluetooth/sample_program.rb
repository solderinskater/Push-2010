require "ruby_bluetooth"

#what to do if we find an arduino
def gotarduino device
	puts "Found Arduino '#{device.name}' with address '#{device.addr}'."
	puts "Inspect: #{device.inspect}"
	meth = device.methods
	meth.each {|m| "device method: #{m}"}
end
loop do
	a = Bluetooth::Devices.scan
	puts "Found #{a.length} bluetooth devices."
	a.each { |device|
		puts "Device: #{device.name}"
	  gotarduino device if  device.name.eql? "ARDUINOBT"
	}
end
