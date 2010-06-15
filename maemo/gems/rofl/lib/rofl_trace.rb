#= this module supplies useful trace output for debugging fun!

module RoflTrace
  #enable vm wide tracing
  def rofl_enable_trace event_regex = /^(call)/
    #this is the Kernel::set_trace_func that we overwrite
    trace_func = Proc.new do |event, file, line, id, binding, classname|
      if event =~ event_regex
        e = {:event=>event,:file=>file,:line=>line,:id=>id,:binding=>binding,:classname=>classname}
        rofl_trace_event_callback e 
      end
    end
    set_trace_func trace_func
    return
  end

  #enable vm wide silent tracing
  def rofl_enable_silent_trace event_regex = /^(call)/
    #this is the Kernel::set_trace_func that we overwrite
    trace_func = Proc.new do |event, file, line, id, binding, classname|
    end
    set_trace_func trace_func
    return
  end

  #disable vm wide tracing
  def rofl_disable_trace
    set_trace_func nil
  end

  #fires when there is a new trace event
  def rofl_trace_event_callback trace_event
    puts "new trace:"
    trace_event.each { |n,t| puts "#{n}: #{t.inspect}"}  
  end
end
