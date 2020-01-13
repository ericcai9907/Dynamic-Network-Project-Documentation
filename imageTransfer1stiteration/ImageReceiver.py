import socket               # Import socket module
import time

s = socket.socket()             # Create a socket object
host = "192.168.0.196"  #Ip address that the TCPServer  is there
port = 53000                     # Reserve a port for your service every new transfer wants a new port or you must wait.

s.connect((host, port))
s.send(bytes("Hello Client!",'utf-8'))

with open('done.jpg', 'wb') as f:
    print('file opened')
    while True:
        print('receiving data...')
        data = s.recv(409600000)
        #print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)
        if str(data,'utf-8') == "DONE":
        	break

f.close()

g = str(time.time())
s.send(bytes(g,'utf-8'))
print("TIMESTAMP SENT")

print('Successfully get the file')
s.close()
print('connection closed')
