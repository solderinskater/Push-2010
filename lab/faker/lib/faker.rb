# Will connect to dbus and offer artificial sensor data

require 'rubygems'
require 'rofl' # http://github.com/pangdudu/rofl
require 'dbus' # http://github.com/pangdudu/ruby-dbus
require 'dbus_client' # http://github.com/pangdudu/dbus-client
require 'sensor'

# connects to dbus and offers fake sensor data
class Faker
	include DBusClient
	
	def initialize
		# dbus relevant stuff
		@dbus_session = DBus::RemoteBus.new("tcp:host=0.0.0.0,port=1337")
		@sensor_service = @dbus_session.request_service("org.sskaters.Sensors")
		# sensor setup 
		gyro = Sensor.new "3-dim-gyroscope"
		@gyro_sensor = DSensor.new gyro,"/org/sskaters/Sensors/Gyroscope"
		# export it to the service
		@sensor_service.export(@gyro_sensor)
		# start pacemaker
		pacemaker 30 # supplied int is frequency in hertz
	end
	
	# update sensors and emit "newData" signals
	def update_sensors
		# get new data from sensor
		gx = @gyro_sensor.sensor.levels[:x].level
		gy = @gyro_sensor.sensor.levels[:y].level
		gz = @gyro_sensor.sensor.levels[:z].level
		# emit a signal with sensordata
		@gyro_sensor.newData gx,gy,gz
	end
	
	# pacemaker running in a seperate thread doing stuff with a given frequency
	def pacemaker frequency # in hertz
		frac = 1.0/frequency
		Thread.new do
			loop do
				update_sensors # well, u guessed it
				sleep frac # we assume that the operations are executed in zero time 
			end
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
  def initialize sensor,path
    super path
    @sensor = sensor
  end  
  # create a dbus interface
  dbus_interface "org.sskaters.Sensors.Interface" do
    # creates a signal in the interface:
    dbus_signal :newData, "x:d, y:d, z:d" # x,y,z as double
    # creates a poll_sensor method in the interface:
    dbus_method :poll_sensor do
      dlog "sensor polled"
    end
  end # end of the dbus interface
end

# get the party started 
faker = Faker.new
faker.dbus_main
