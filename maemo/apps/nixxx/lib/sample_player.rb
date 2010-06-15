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
require 'rofl'
require 'thread'

# Push sound sample class
class Sample
	include Rofl
	
	attr_accessor :played,:playbin,:ready
	
	def initialize samplename,start_vol,paused,sound_folder
		@sound_folder = sound_folder
		@played = false
		@ready = false
		@paused = paused
		build_pipeline samplename,start_vol
	end
	
	# mutexed pipeline getter
	def pipeline
		@pipeline_mutex = Mutex.new unless @pipeline_mutex
		@pipeline_mutex.synchronize do		
		end
		return @pipeline 
	end

	# mutexed audiosink getter
	def audiosink
		@audiosink_mutex = Mutex.new unless @audiosink_mutex
		@audiosink_mutex.synchronize do
		end
		return @audiosink
	end

	# mutexed samplebin getter
	def samplebin
		@samplebin_mutex = Mutex.new unless @samplebin_mutex
		@samplebin_mutex.synchronize do
			return @samplebin
		end
		return @samplebin
	end

	# mutexed audiosrc getter
	def audiosrc
		@audiosrc_mutex = Mutex.new unless @audiosrc_mutex
		@audiosrc_mutex.synchronize do
		end
		return @audiosrc
	end

	# mutexed decoder getter
	def decoder
		@decoder_mutex = Mutex.new unless @decoder_mutex
		@decoder_mutex.synchronize do
		end
		return @decoder
	end

	# mutexed audioconverter getter
	def audioconverter
		@audioconverter_mutex = Mutex.new unless @audioconverter_mutex
		@audioconverter_mutex.synchronize do
			return @audioconverter
		end
	end

	# mutexed volume getter
	def volume
		@volume_mutex = Mutex.new unless @volume_mutex
		@volume_mutex.synchronize do
		end
		return @volume
	end
	
	# build the samplehash
	def build_pipeline samplename,start_vol
		
		filename = "#{@sound_folder}#{samplename}.mp3"
		puts "Adding new sample '#{samplename}' from file '#{filename}'"
		
		# create a new pipeline to hold the elements
		@pipeline = Gst::Pipeline.new
		#@pipeline = Gst::ElementFactory.make('playbin')
		@audiosink = Gst::ElementFactory.make("pulsesink","audiosink")
		
		# add objects to the main pipeline, all other objects will come later through add_sample
		pipeline.add(audiosink)
		pipeline.pause
		
		# we will put all our stuff into the bin
		@samplebin = Gst::ElementFactory.make("bin", samplename)
		
		# create a file reader
		@audiosrc = Gst::ElementFactory.make("filesrc", "audiosrc")
		audiosrc.location = filename

		# now it's time to get the decoder (decodebin is auto-magical)
		#decodebin = "decodebin"
		decodebin = "nokiamp3dec"
		@decoder = Gst::ElementFactory.make(decodebin,"decoder")
		
		# and an audio convertor
		@audioconverter = Gst::ElementFactory.make("audioconvert","audioconverter")
		
		# our volume control
		@volume = Gst::ElementFactory.make("volume","volume")
		
		# set initial volume
		volume.volume = start_vol
		
		# add the elements to the samplebin
		samplebin.add(audiosrc)
		samplebin.add(decoder)
		samplebin.add(audioconverter)
		samplebin.add(volume)
		#samplebin.add(level)
		
		# link what can already be linked
		audiosrc >> decoder
		audioconverter >> volume #>> level
		
		@connecting_signal = false
		
		puts "Initial linking done."
		
		puts "Now adding ghost pads."
		# inherit the level src pad for our bin
		volume_src = volume.get_pad("src")

		ghost_src = Gst::GhostPad.new("src", volume_src)
		samplebin.add_pad(ghost_src)
		puts "Ghost pads added."

		# pause while we do the last linking an adding
		pipeline.pause
		samplebin.sync_state_with_parent
		pipeline.add(samplebin)
		samplebin >> audiosink

		# now we need to prepare the connection of decoder and converter (like decoder >> audioconverter)
		decoder.signal_connect("new-decoded-pad") do |element, pad|
		  @connecting_signal = true
		  pipeline.pause
		  sink_pad = @audioconverter.get_pad("sink")
		  if pad.nil?
		  	puts "pad inspect: #{pad.inspect}"
		  	puts "element inspect: #{element.inspect}"
		  else
		  	pad.link(sink_pad)
			  puts "Decoder and audioconverter linked."
		  end
		  unless @paused
				puts "Sample is setup will now play it."
				pipeline.pause
				pipeline.play
			else
				puts "Sample is setup and paused."
			end
			@ready = true
			@connecting_signal = false
		end

		# and finally play the sample again, if not already playing
		while !@ready
			sleep 0.1
			if !@connecting_signal
				@connecting_signal = true
				# CAUTION!!! if we don't sync here, we'll get a segfault
				sync_states
			end
		end
		#puts "Added new sample: #{samplename}"
	end
	
	def sync_states
		audiosrc.sync_state_with_parent
		decoder.sync_state_with_parent
		audioconverter.sync_state_with_parent
		volume.sync_state_with_parent
		samplebin.sync_state_with_parent
	end
	
end

# Push sound sample player class
class SamplePlayer
	include Rofl

	#attr_accessor :samples

  def initialize sound_folder
  	@sound_folder = sound_folder
  	@samples = {}
  	@sample_mutex = Mutex.new
  	@busy = false
    Gst.init
    add_sample "startup"
  end

	def samples
		@sample_mutex.synchronize do
			return @samples
		end
	end

  # adds a new sample source to the pipeline
  def add_sample samplename,start_vol=1.0,paused=false
		@busy = true
		sample = Sample.new samplename,start_vol,paused,@sound_folder
		samples[samplename] = sample
		@busy = false
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
    	if samples[samplename].played
    	  puts "rewind '#{samplename}'"
    		sample_rewind samplename,1.0,false
  	  	samples[samplename].played = true
  	  else
  	    puts "directplay '#{samplename}'"
  	  	samples[samplename].pipeline.play
  	  	samples[samplename].played = true
  	  end
    else
      wlog "No pipeline for: '#{samplename}', sorry."    
    end 
  end
  
  # pause a specific sample
  def pause_sample samplename
  	samples[samplename].pipeline.pause if samples.has_key? samplename
  end
  
  # rewind a sample
  def sample_rewind samplename,volume=1.0,paused=true
    if samples.has_key? samplename
			samples[samplename].pipeline.stop
			samples.delete samplename
			add_sample samplename,volume,paused
		end
  end
  
  # seek to a position
  def sample_seek_to samplename,time
  	if samples.has_key? samplename
			t,ff,s,n = Gst::Format::TIME, Gst::Seek::FLAG_FLUSH, Gst::SeekType::SET, Gst::SeekType::NONE
		  samples[samplename].pipeline.pause
		  samples[samplename].sync_states
		  puts "now trying to seek"
			samples[samplename].decoder.seek(1.0,t,ff,s,time,n,0)
			puts "seek succeded!"
			samples[samplename].pipeline.get_state(100 * Gst::MSECOND)
			samples[samplename].pipeline.play
			samples[samplename].sync_states
    else
    	wlog "failed to get pipeline"
    end
  end

end

def test
	sp = SamplePlayer.new "../sounds/"
	sleep 1
	sp.add_sample "good",1.0,true
	sp.play_sample "good"
	sleep 1
	sp.play_sample "good"
	sleep 3
	sp.play_sample "good"
	sp.play_sample "good"
	sp.play_sample "good"
	sp.play_sample "good"
	sp.play_sample "good"
	sp.play_sample "good"
	#sp.sample_seek_to "good",0
	loop { sleep 1 }
end

test
