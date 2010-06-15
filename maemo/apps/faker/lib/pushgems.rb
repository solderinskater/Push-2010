#path of the gem directory on the maemo device
gempath = "/opt/pushitcode/pushitrealgood/maemo/gems"
#list of gems we want to include
gems = ["rofl","ruby-dbus","dbus-client"]
#now we add the gems to the interpreter include variable ($:)
gems.each do |gem|
  $: << "#{gempath}/#{gem}/lib"
end
