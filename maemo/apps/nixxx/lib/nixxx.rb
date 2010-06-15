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

#require 'sample_player'
require 'nokia_player'
require 'dbus'
require 'dbus_client'
require 'rofl'

# simple mixer we use when reacting to dbus signals
class Mixer

  attr_accessor :player

  def initialize sound_folder=""
    @player = SamplePlayer.new sound_folder
  end

  def add_sound_sample samplename,start_vol=0.9
  	# add_sample method parameters: samplename,start_vol=1.0,paused=false
    @player.add_sample(samplename,start_vol)
  end

end

# Listen to DBus signals and enemy communications
class Echelon
	include DBusClient
	include Rofl

	def initialize
		@listeners = []
		@bus = DBus::RemoteBus.new('tcp:host=localhost,port=1337')
		@trick_interface = "net.prometoys.solderinskater.TrickService"
		@trick_service = "/net/prometoys/solderinskater/TrickService/DbusTrickObject"
		initialize_signal_listener
		start_dbus
	end

	# setup signal listener
	def initialize_signal_listener
		#subscribe on newData signals
		mr = DBus::MatchRule.new
		mr.type = "signal"
		mr.interface = @trick_interface
		mr.path = @trick_service
		@bus.add_match(mr) { |signal| inform_listeners signal }
	end

	# handle an incoming signal
	def inform_listeners signal
		#dlog "Incoming Signal: '#{signal.inspect}'"
		@listeners.each { |l| l.handle_signal signal }
	end

	# add a listener
	# CAUTION: listener must have a method named 'handle_signal signal'
	def add_listener listener
		@listeners << listener unless @listeners.include? listener
	end

	# go into dbus main loop
	def start_dbus
		#and go into dbus main loop
		Thread.new { dbus_main @bus }
	end

end

# NiXXX
class Nixxx
	include Rofl

	attr_accessor :music_mixer,:sound_mixer,:echelon

	def initialize
		if File.exist? "../music/broken.mp3"
			@soundtrack = "broken"
			@music_mixer = Mixer.new "../music/"
			@music_mixer.add_sound_sample(@soundtrack,0.9)
		end
		@sound_mixer = Mixer.new "../sounds/"
		@echelon = Echelon.new
		@echelon.add_listener self
		load_sound_samples
	end

	# handle an incoming signal, get's called by echelon dbus client
	def handle_signal signal
		#dlog "Incoming Signal: '#{signal.inspect}'"
    signal_router signal
	end

  # route signals to corresponding methods
  def signal_router signal
    case signal.member
      when "ShoutSignal" then shout_handler signal
      when "MusicSignal" then music_handler signal
      when "LevelSignal" then level_handler signal
      when "MusicCommandSignal" then music_command_handler signal
      #else dlog "Don't know what to do with signal: '#{signal.member.inspect}'"
    end
  end

  # handle a shout signal
  def shout_handler signal
    samples = signal.params.first
    #dlog "samples to play: #{samples.inspect}"
    samples.each do |samplename|
    	play_sound_sample samplename
    	#sleep 1.5 # HACK unitl we know the actual sample lengths
    end
  end

  # handle a music signal
  def music_handler signal
  	params = signal.params
  	#dlog "music handler received params: '#{params.inspect}'"
  end

  # handle a level signal
  def level_handler signal
    samples = signal.params.first
    samplename = "level_#{samples}"
    dlog "submit level_string: #{samplename}"
    #sleep 1.5 # HACK unitl we know the actual sample lengths
    play_sound_sample samplename
  end

  # handle a music command signal
  def music_command_handler signal
  	params = signal.params.first
  	#dlog "music handler received params: '#{params.inspect}'"
  	if @soundtrack
  		@music_mixer.player.play_sample @soundtrack if params.include? "play"
  		@music_mixer.player.pause_sample @soundtrack if params.include? "pause"
  		@music_mixer.player.stop_sample @soundtrack if params.include? "stop"
  	end
  end

  # let sound_mixer play a sound sample
  def play_sound_sample samplename
    if @samples.has_key? samplename
      filename = @samples[samplename][rand(@samples[samplename].length)]
      @sound_mixer.player.play_sample filename
      sleep 0.4
    else
      wlog "'#{samplename}' not playable, samples: #{@samples.inspect}"
    end
  end

	# load the sound samples
	def load_sound_samples
    # TODO HACK bekannte samples, dynamisch erweitern oder ganz raus
    @samples = {"ollie" => ["p_ollie"],
                "good" => ["a_awesome","a_herewego","a_nicestyle","a_superockin","a_yeah","a_yougotit",
                           "p_awesome","p_herewego","p_nicestyle","p_yeah","p_yougotit"],
                "180" => ["a_180"],
                "level_1" => ["a_level1"],
                "level_2" => ["a_level2"],
                "level_3" => ["a_level3"],
                "level_4" => ["a_level4"],
                "level_5" => ["a_level5"]
                }

    # parameters samplename,volume,paused
		# if paused = true, the sample starts paused
    @samples.each do |k,v|
      v.each { |s| @sound_mixer.add_sound_sample(s,0.9) }
    end
    @music_mixer.player.play_sample @soundtrack if @soundtrack
	end

end

n = Nixxx.new
#sleep 10
#n.music_mixer.player.pause_sample "broken"
#sleep 10
#n.music_mixer.player.play_sample "broken"
loop { sleep 1 }
