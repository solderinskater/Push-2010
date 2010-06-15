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
 
class SongPlayer < Gst::Pipeline
  def self.songs_dir= dir
    metaclass = class << self; self; end
    metaclass.send :define_method, :songs_dir do dir end
  end

  def self.songs_dir
    raise RuntimeError, "Call #{self}.songs_dir = dir first"
  end

  def initialize
    super()
    src = Gst::ElementFactory.make('filesrc')
    dec = Gst::ElementFactory.make('decodebin')
    conv = Gst::ElementFactory.make('audioconvert')
    resmp = Gst::ElementFactory.make('audioresample')
    sink = Gst::ElementFactory.make('autoaudiosink')

    @src = src

    add src, dec, conv, resmp, sink
    src >> dec
    conv >> resmp >> sink

    dec.signal_connect 'new-decoded-pad' do |elem, pad|
      pad.link conv['sink']
    end
  end

  def seek_to time
    seek 1.0, Gst::Format::TIME, Gst::Seek::FLAG_FLUSH, Gst::SeekType::SET,
          time, Gst::SeekType::NONE, 0
  end

  def song= filename
    @src.location = filename
  end
end

s = SongPlayer.new
s.song = ARGV[0]
s.play
loop { sleep 1 }
