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

require 'gst'
Gst.init

# Push sound sample class
class Sample
	
	attr_accessor :played,:ready
	attr_accessor :pipeline,:volume
	
	def initialize samplename,start_vol,sound_folder
		@sound_folder = sound_folder
		@played = false
		@ready = false
		build_pipeline samplename,start_vol
	end
	
	# build the samplehash
	def build_pipeline samplename,start_vol
		filename = "#{@sound_folder}#{samplename}.mp3"
		
		puts "Adding new sample '#{samplename}' from file '#{filename}'"
		
		pipeline = Gst::Pipeline.new
		# try: sh gst-launch-0.10 filesrc location=../sounds/startup.mp3 ! mp3parse ! nokiamp3dec ! audioconvert ! pulsesink
		
		# create a file reader
		audiosrc = Gst::ElementFactory.make("filesrc")
		audiosrc.location = filename
		
		# audio format parser
		parser = Gst::ElementFactory.make("mp3parse")
		
		# audio decoder
		decoder = Gst::ElementFactory.make("nokiamp3dec")
		
		# and an audio convertor
		audioconverter = Gst::ElementFactory.make("audioconvert")
		
		# and an audio resampler
		audioresample = Gst::ElementFactory.make("audioresample")
		
		# our volume control
		volume = Gst::ElementFactory.make("volume")
		# set initial volume
		volume.volume = 0.9
		
		# audiosink
		audiosink = Gst::ElementFactory.make("pulsesink")		
		
		# add the elements to the samplebin
		pipeline.add(audiosrc)
		pipeline.add(parser)
		pipeline.add(decoder)
		pipeline.add(audioconverter)
		#pipeline.add(audioresample)
		pipeline.add(volume)
		pipeline.add(audiosink)
		
		audiosrc >> parser >> decoder	>> audioconverter >> volume >> audiosink
		#pipeline.pause
		
		@volume,@pipeline = volume,pipeline
		
		@ready = true
		
		#@pipeline.play	
	end
		
end

# Push sound sample player class
class SamplePlayer

	#attr_accessor :samples

  def initialize sound_folder
  	@sound_folder = sound_folder
  	@samples = {}
  	@sample_mutex = Mutex.new
    #add_sample "startup"
    #play_sample "startup"
  end

	def samples
		@sample_mutex.synchronize do
			return @samples
		end
	end

  # adds a new sample source to the pipeline
  def add_sample samplename,start_vol=0.1
		sample = Sample.new samplename,start_vol,@sound_folder
		samples[samplename] = sample
  end

  # adjust the volume of a specific sample
  def sample_volume samplename, volume
    if samples.has_key? samplename
      samples[samplename].volume.volume = volume
    else
    	wlog "Sample with name '#{samplename}' not found, could not set volume!"
    end
  end

  # play a specific sample
  def play_sample samplename
    puts "Trying to play: '#{samplename}'"
    if samples.has_key? samplename
    	if samples[samplename].played && samples[samplename].ready
    	  puts "rewind '#{samplename}'"
    		while !samples[samplename].ready && samples[samplename].played
					sleep 0.1
				end
    		sample_rewind samplename,0.9
  	  else
  	    puts "directplay '#{samplename}'"
  	  end
  	  
  	  samples[samplename].pipeline.get_state(100 * Gst::MSECOND)
  	  samples[samplename].pipeline.play
  	  samples[samplename].played = true
    else
      wlog "No pipeline for: '#{samplename}', sorry."    
    end 
  end
  
  # pause a specific sample
  def pause_sample samplename
  	if samples.has_key? samplename
  		samples[samplename].pipeline.pause
  		samples[samplename].ready = true
  	end 
  end

  # stop a specific sample
  def stop_sample samplename
  	if samples.has_key? samplename
  		samples[samplename].pipeline.stop
  		samples[samplename].ready = false
  	end
  end
  
  # rewind a sample
  def sample_rewind samplename,volume=0.9
    if samples.has_key? samplename
			samples[samplename].pipeline.stop
			samples[samplename] = nil
			add_sample samplename,volume
		end
  end
  
  # seek to a position
  def sample_seek_to samplename,time
  	if samples.has_key? samplename
			t,ff,s,n = Gst::Format::TIME, Gst::Seek::FLAG_FLUSH, Gst::SeekType::SET, Gst::SeekType::NONE
		  samples[samplename].pipeline.pause
		  puts "now trying to seek"
			samples[samplename].pipeline.seek(1.0,t,ff,s,time,n,0)
			puts "seek succeded!"
			samples[samplename].pipeline.get_state(100 * Gst::MSECOND)
			samples[samplename].pipeline.play
    else
    	wlog "failed to get pipeline"
    end
  end

end

def test
	sp = SamplePlayer.new "../sounds/"
	sleep 1
	sp.add_sample "good",1.0
	sp.play_sample "good"
	sleep 1
	sp.play_sample "good"
	sp.play_sample "good"
	sp.play_sample "good"
	sp.play_sample "good"
	sp.play_sample "good"
	sp.play_sample "good"
	#sleep 1 
	#sp.sample_seek_to "good",0
	loop { sleep 1 }
end

def simple_test
		filename = "../sounds/startup.mp3"
		pipeline = Gst::Pipeline.new
		# try: sh gst-launch-0.10 filesrc location=../sounds/startup.mp3 ! mp3parse ! nokiamp3dec ! audioconvert ! pulsesink
		
		pipeline.pause
		
		# create a file reader
		audiosrc = Gst::ElementFactory.make("filesrc")
		audiosrc.location = filename
		
		# audio format parser
		parser = Gst::ElementFactory.make("mp3parse")
	
		# audio decoder
		decoder = Gst::ElementFactory.make("nokiamp3dec")
		
		# and an audio convertor
		audioconverter = Gst::ElementFactory.make("audioconvert")
		
		# and an audio resampler
		audioresample = Gst::ElementFactory.make("audioresample")
		
		# our volume control
		volume = Gst::ElementFactory.make("volume")
		# set initial volume
		volume.volume = 1.0
		
		# audiosink
		audiosink = Gst::ElementFactory.make("pulsesink")		
		
		# add the elements to the samplebin
		pipeline.add(audiosrc)
		pipeline.add(parser)
		pipeline.add(decoder)
		pipeline.add(audioconverter)
		pipeline.add(audioresample)
		pipeline.add(volume)
		pipeline.add(audiosink)
		
		audiosrc >> parser >> decoder	>> audioconverter >> audioresample >> volume >> audiosink
		
		pipeline.play
end

#test
#loop { sleep 1 }
