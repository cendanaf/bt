import os
import socket

addr = 'E8:B1:FC:F5:16:02'
port = 4

btAddr = '34:43:0b:0b:bd:9b'

bufferSize = 1024

#cmd = 'hcitool rssi ' + btAddr
command = 'sudo iw wlan0 scan | grep "SSID: Nucleus" -B2'

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
server.connect((addr, port))

while True:
    cmd = server.recv(bufferSize)
    # process command
    cmd = str(cmd, 'utf-8')
    print(cmd)
    res = cmd
    if cmd == 'quit':
        server.send(bytes(cmd, 'utf-8'))
        break
    elif cmd == 'u':
        res = 'u'
        #res += os.popen(command).read()[-3:-1]
        res += os.popen(command).read()[8:14]
        server.send(bytes(res, 'utf-8'))
    else:
        server.send(bytes(res,'utf-8'))
    
print('Closing server socket')
server.close()
