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

require 'logger'

###
#	Rofl Logger Module
###
module Rofl
	#check if there already is a logger, kind of a constructor
	def rofl_logger_check
		@debugname,@logger = nil,nil
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

end

###
#	Rofl Logger Module - END
###
