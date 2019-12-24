import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(('127.0.0.1', 60000))
s.close()


#plot frame thread server listen to wait for signal and then refresh