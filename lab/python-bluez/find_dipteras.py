import bluetooth

target_prefix = "Diptera"
target_address = None

nearby_devices = bluetooth.discover_devices()
print nearby_devices

for bdaddr in nearby_devices:
    device_name = bluetooth.lookup_name( bdaddr )
    if device_name is not None:
        if device_name.startswith(target_prefix):
            print "Found Diptera bluetooth device ", device_name, bdaddr
