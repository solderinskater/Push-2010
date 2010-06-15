# Will connect to dbus and offer artificial sensor data

require 'rubygems'
#require 'rofl' # http://github.com/pangdudu/rofl
require 'serialport'
require 'dbus' # http://github.com/pangdudu/ruby-dbus
require 'dbus_client' # http://github.com/pangdudu/dbus-client

# connects to dbus and offers sensor data from a serialport 
class SuperCerial
	include DBusClient
	
	def initialize
		# dbus relevant stuff
		@dbus_session = DBus::RemoteBus.new("tcp:host=0.0.0.0,port=1337")
		@sensor_service = @dbus_session.request_service("org.sskaters.Sensors")
		# sensor setup 
		@gyro_sensor = DSensor.new "/org/sskaters/Sensors/Gyroscope"
		# export it to the service
		@sensor_service.export(@gyro_sensor)
		#init serial subsystem
		init_serial
		#get sensor data
		update_sensors
	end
	
	#init serial subsystem
	def init_serial
		#params for serial port
		port_str = "/dev/rfcomm0"  #may be different for you
		baud_rate = 115200
		data_bits = 8
		stop_bits = 1
		parity = SerialPort::NONE
		@sp = SerialPort.new(port_str, baud_rate, data_bits, stop_bits, parity)
	end
	
	# update sensors and emit "newData" signals
	def update_sensors
		Thread.new do 
			#just read forever
			while true do
  			line = @sp.readline
  			# "x507y512z605X470Y475Z380\r\n"
  			d = line.strip.split(/[xyzXYZ]/)
  			puts "DATA: #{d.inspect}"
  			# emit a signal with sensordata
  			begin
  				@gyro_sensor.newData d[1],d[2],d[3],d[4],d[5],d[6]
  			rescue
  				puts "failed to submit data"
  			end
			end
			@sp.close
		end
	end
	
	# blocking dbus main loop, needed for signal handling
	def dbus_main
	  main = DBus::Main.new
	  main << @dbus_session
	  main.run
	end
end

# sensor object we export to dbus
class DSensor < DBus::Object
  attr_reader :sensor
  def initialize path
    super path
  end  
  # create a dbus interface
  dbus_interface "org.sskaters.Sensors.Interface" do
    # creates a signal in the interface:
    dbus_signal :newData, "x:d, y:d, z:d, X:d, Y:d, Z:d" # x,y,z,X,Y,Z as double
    # creates a poll_sensor method in the interface:
    dbus_method :poll_sensor do
      dlog "sensor polled"
    end
  end # end of the dbus interface
end

# get the party started 
sc = SuperCerial.new
sc.dbus_main
