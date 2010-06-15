require 'rubygems'
require 'mp3info'
require 'gst'

class Player

  attr_accessor :pipeline

  def initialize filename
    @mp3info = get_mp3info filename
    puts "opening file: #{filename}"
    unless File.exist? filename
      puts "File #{filename} not found, sorry."
    end
    Gst.init
    # create a new pipeline to hold the elements
    @pipeline = Gst::Pipeline.new
    # create a disk reader
    @audiosrc = Gst::ElementFactory.make("filesrc")
    @audiosrc.location = filename
    # now it's time to get the decoder (decodebin is auto-magical)
    @decoder = Gst::ElementFactory.make("decodebin")
    #and an audio convertor
    @audioconverter = Gst::ElementFactory.make("audioconvert")
    # and an audio sink
    @audiosink = Gst::ElementFactory.make("pulsesink")
    # add objects to the main pipeline
    @pipeline.add(@audiosrc, @decoder, @audioconverter, @audiosink)
    # link elements
    @audiosrc >> @decoder
    @audioconverter >> @audiosink
    #now we need to connect the decoder and converter
    @decoder.signal_connect("new-decoded-pad") do |element, pad|
      sink_pad = @audioconverter.get_pad("sink")
      pad.link(sink_pad)
    end
    @pipeline.pause
  end

  #seek (goto a position in the audio file)
  #fraction is the fraction of the track we want to seek to
  def seek fraction
    new_pos = (@mp3info.length * fraction)
    puts "seeking to #{new_pos}"
    # Send the new position to the lastest sink pad.
    @pipeline.pause
    @pipeline.seek(1.0, Gst::Format::Type::TIME,
                   Gst::Seek::FLAG_FLUSH.to_i | 
                   Gst::Seek::FLAG_KEY_UNIT.to_i, 
                   Gst::Seek::TYPE_SET, 
                   new_pos*Gst::SECOND, 
                   Gst::Seek::TYPE_NONE, -1)
    @pipeline.play
  end

  #basic player methods
  def play
    @thread = Thread.new do
      @pipeline.play
    end
    @thread.run
    puts "Now playing: #{@audiosrc.location}"
  end

  def pause
    @pipeline.pause
  end

  def stop
    @pipeline.stop
  end

  def get_mp3info filename
    info = nil
    Mp3Info.open(filename) do |mp3info|
      info = mp3info
    end
    return info
  end

 def get_mp3info filename
  info = nil
  Mp3Info.open(filename) do |mp3info|
    info = mp3info
  end
  return info
 end 
end

#testing

def test
  p = Player.new "music.mp3"
  p.play
end

test
loop do
 sleep 1
end
