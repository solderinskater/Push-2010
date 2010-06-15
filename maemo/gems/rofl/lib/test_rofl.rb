require 'rofl'
include Rofl

class Test
  def initialize
    dlog "initialize"
  end
  def call_hello_world
    other_method
    hello_world
    other_method
  end
  def hello_world
    other_method
    dlog "hello world!"
    other_method
  end
  def other_method
    ilog "other method called"
  end
end

test = Test.new 
test.rofl_log_level "warning"
test.call_hello_world
