require 'logger'
require 'rofl_trace'
#little happy logger module
module Rofl
  include RoflTrace

  attr_accessor :debugname,:logger
  
  #check if there already is a logger, kind of a constructor
  def rofl_logger_check
    if @logger.nil?
      #to stop output from getting messy, we use a logger
      @logger = Logger.new(STDOUT)
      @logger.level = Logger::DEBUG
      #@logger.datetime_format = "%Y-%m-%d %H:%M:%S" #useful for logging to a file
      @logger.datetime_format = "%H:%M:%S" #useful for debugging
      @debugname = self.class if @debugname.nil? #only used to inform the user
      @tracing = false
      #enable tracing
      if @tracing
        rofl_enable_silent_trace
      end
    end
  end
  
  #set the debug level
  def rofl_log_level level=""
    @logger.level = Logger::DEBUG if level.eql? "debug"
    @logger.level = Logger::INFO if level.eql? "info"
    @logger.level = Logger::WARN if level.eql? "warning"
    @logger.level = Logger::ERROR if level.eql? "error"
    puts "ROFL-LOG-LEVEL: #{@logger.level}" 
  end
  
  #error message
  def elog text="error" 
    rofl_logger_check #check if logger is setup
    @logger.error "#{@debugname}.#{rofl_meth_trace.to_s}: #{text.to_s}"
  end
  
  #warning
  def wlog text="warning"
    rofl_logger_check #check if logger is setup
    @logger.warn "#{@debugname}.#{rofl_meth_trace.to_s}: #{text.to_s}"
  end
  
  #info message
  def ilog text="info"
    rofl_logger_check #check if logger is setup
    @logger.info "#{@debugname}.#{rofl_meth_trace.to_s}: #{text.to_s}"
  end
  
  #debug message
  def dlog text="debug"
    rofl_logger_check #check if logger is setup
    @logger.debug "#{@debugname}.#{rofl_meth_trace.to_s}: #{text.to_s}"
  end
  
  #get method call trace
  def rofl_meth_trace
    last_meth_name = "notrace"
    skip = 2 #indicates how many items we skip in the execution stack trace
    call_trace = caller(skip)
    regexp = /\`.*?\'/
    last_meth = call_trace[0][regexp]
    last_meth_name = last_meth.delete("\`") unless last_meth.nil?
    last_meth_name = last_meth_name.delete("\'") unless last_meth_name.nil?
    return last_meth_name
  end
  
  #check if we or an object are ready to rofl
  def rofl? object=self
    has_rofl = (defined? object.rofl?).eql? "method"
    dlog "object of class: #{object.class} is rock'n'rofl." if has_rofl
    return has_rofl
  end
end

#finally we just include ourselves, a little dirty ... what the hell :)
include Rofl

#and check, if we're ready to go
rofl_logger_check
