# purpose of this code is to supply us with semi-plausible fake sensor data

# class representing a sensor unit
class Sensor
	attr_reader :levels # hash with current sensor levels
	attr_reader :id
	
	def initialize identificator
		@id = identificator
		@levels = {}
		@levels[:x] = SignalSource.new [-10,10],50,5
		@levels[:y] = SignalSource.new [-10,10],15,3
		@levels[:z] = SignalSource.new [-10,10],25,7
	end
end

# class representing a signal source
class SignalSource

	def initialize spectrum, frequency, noise_level
		@spectrum = spectrum # e.g. [-1,1]
		@range = @spectrum[1]-@spectrum[0]
		@frequency = 1.0/frequency # internal frequency
		@noise_level = noise_level # multipliactor
		@time = 0.0 # signal internal timer 
	end
	
	#get the current signal level
	def level
		@time = (@time + @frequency) % Math::PI
		return noise + @spectrum[0] + @range * shape(@time)
	end
	
	#general signal shape (depends on time)
	def shape time
		return Math.sin time
	end
	
	#get the noise level, -1..1 if noise_level is 1
	def noise
		return 2.0*(0.5-rand)*@noise_level
	end
end
