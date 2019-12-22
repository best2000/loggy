
import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                 
s.connect(("www.python.org" , 80))
s.sendall(b'GET http://www.python.org HTTP/1.0\n\n')
print (s.recv(4096))
s.close()