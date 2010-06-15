import bluetooth

bd_addr = "00:06:66:02:F1:FC"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

print "Connected: ", bd_addr

sock.close()
