=begin
	This is the gui we'll use to annotate the sensor time series data with
=end

require 'rubygems'
require 'rofl'
require 'serialport'
require 'dbus_client' # http://github.com/pangdudu/dbus-client
require 'Qt4'

class Gui < Qt::Widget
	include DBusClient
  
  attr_reader :width,:height
  attr_reader :x_delta,:mousex,:mousey
  
  def initialize(width,height,parent = nil)
    super()
    @width,@height = width,height
    resize(@width,@height)
    @current_color = 0
    #now some gui specific stuff
    setPalette(Qt::Palette.new(Qt::Color.new(250, 250, 250)))
    setAutoFillBackground(true)
    #cursor settings
    @cur1 = self.cursor
    @cur2 = Qt::Cursor.new(Qt::PointingHandCursor)
    self.mouseTracking = true
    #we'll need this for painting the graphs
    @xdelta = 0
    #setup painter paths
    init_paths
    #setup dbus and go into dbus main loop
    init_dbus
    #setup serial
    init_serial
  end
  
  #setup painter path later used for painting
  def init_paths
    @path_sgx = Qt::PainterPath.new
    @path_sgx.moveTo 0,0
    @path_sgy = Qt::PainterPath.new
    @path_sgy.moveTo 0,0
    @path_sgz = Qt::PainterPath.new
    @path_sgz.moveTo 0,0
    @path_acc1 = Qt::PainterPath.new
    @path_acc1.moveTo 0,0
    @path_acc2 = Qt::PainterPath.new
    @path_acc2.moveTo 0,0
  end
  
  #add sensor data listeners and drop into dbus main loop
  def init_dbus
  	dbus = DBus::RemoteBus.new("tcp:host=0.0.0.0,port=1337")
		#subscribe on newData signals
		mr = DBus::MatchRule.new
		mr.type = "signal"
		mr.interface = "org.sskaters.Sensors.Interface"
		mr.path = "/org/sskaters/Sensors/Gyroscope"
		dbus.add_match(mr) { |data| repaint_gyroscope data.params }
		#and go into dbus main loop
		Thread.new { dbus_main dbus }
  end

  #add serial sensor data listeners
  def init_serial
  	dbus = DBus::RemoteBus.new("tcp:host=0.0.0.0,port=1337")
		#subscribe on newData signals
		mr = DBus::MatchRule.new
		mr.type = "signal"
		mr.interface = "org.sskaters.Sensors.Interface"
		mr.path = "/org/sskaters/Sensors/Gyroscope"
		dbus.add_match(mr) { |data| repaint_gyroscope data.params }
		#and go into dbus main loop
		Thread.new { dbus_main dbus }
  end
  
  #get's called by incoming sensor data and repaints the gyroscope graph
  def repaint_gyroscope data
  	#dlog "incoming data: #{data.inspect}"
  	@xdelta += 1
  	@path_sgx.lineTo(@xdelta,(data[0]-500)/2) # gyro x
  	@path_sgy.lineTo(@xdelta,(data[1]-500)/2) # gyro y
  	@path_sgz.lineTo(@xdelta,(data[2]-500)/2) # gyro z
  	@path_acc1.lineTo(@xdelta,(data[3]-500)/2) # gyro y
  	@path_acc2.lineTo(@xdelta,(data[4]-500)/2) # gyro z
  	update
  end
  
  #gets called when a repaint is necessary
  def paintEvent(event)
  	paint_paths
  end
  
  #outsourced legend painting
  def paint_paths
    p = Qt::Painter.new(self)
    #p.setRenderHint(Qt::Painter::HighQualityAntialiasing)
    p.setBrush Qt::NoBrush
    penx = Qt::Pen.new(Qt::SolidLine)
    penx.setColor Qt::Color.new(50, 50, 160)
    penx.setWidth 1
    peny = Qt::Pen.new(Qt::SolidLine)
    peny.setColor Qt::Color.new(100, 100, 200)
    peny.setWidth 1
    penz = Qt::Pen.new(Qt::SolidLine)
    penz.setColor Qt::Color.new(150, 150, 240)
    penz.setWidth 1
    path_array = [@path_sgx,@path_sgy,@path_sgz,@path_acc1,@path_acc2]
    n = path_array.size
    i = 1
    path_array.each do |path|
   		p.resetMatrix
    	p.translate(3*@width/4-@xdelta,@height*i/(n+2))
    	p.setPen(penx)
    	p.drawPath path
    	i = i+1
    end
    p.end()
  end

  #mouse press event
  def mousePressEvent event
    if event.buttons == Qt::RightButton
    elsif event.buttons == Qt::LeftButton
      #update
    end
  end
  
  #a mouse move event
  def mouseMoveEvent event
    @mousex,@mousey = event.x,event.y
  end
end

#start the qt application
app = Qt::Application.new(ARGV)
gui = Gui.new(800,700)
#dirty qt timer magic to make ruby threads work
block=Proc.new{ Thread.pass }
timer=Qt::Timer.new(gui)
invoke=Qt::BlockInvocation.new(timer, block, "invoke()")
Qt::Object.connect(timer, SIGNAL("timeout()"), invoke, SLOT("invoke()"))
timer.start(10) #in millis
#end of dirty timer hack
gui.show()
app.exec()
