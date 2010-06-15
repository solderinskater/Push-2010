# Simple dbus client module 

#require 'rubygems' # for !maemo
require 'pushgems'
require 'rofl'
require 'dbus'

module DBusClient
	#get a dbus object from a service
  def get_object_from_service dbus_session,service_name,obj_path,default_iface
    begin
      if running? dbus_session,service_name
        service = dbus_session.service(service_name)
        obj = service.object(obj_path)
        obj.introspect
        obj.default_iface = default_iface
        return obj
      end
      return nil
    rescue
      elog "could not get object:#{obj_path} from service: #{service_name}"
      return nil
    end
  end
  
  #check if a service is running
  def running? dbus_session,service_name
    return dbus_session.proxy.ListNames[0].include? service_name
  end
  
  #list underlying names of a proxy object
  def list_names bus,proxy=nil
    proxy = bus.proxy if proxy.nil?
    dlog "listnames:"
    proxy.ListNames[0].each { |name| dlog name }
  end
  
 	#blocking dbus main loop, needed for signal handling
	def dbus_main dbus_session
	  main = DBus::Main.new
	  main << dbus_session
	  main.run
	end
end
