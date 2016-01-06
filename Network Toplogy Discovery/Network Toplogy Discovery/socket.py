import socket
from socket import *
import thread

Host = "192.168.0.103"
Port = 54500
Buff_size = 1024
s = socket(AF_INET, SOCK_STREAM) 
s.bind((Host,Port))
s.listen(1)
while True:
    client,address = s.accept()
    print('connected from: ', address)
    client.send(str.encode('Welcome to my Chat room!'))
    while True:
        message = client.recv(Buff_size)
        if not message:
            break
        #if message == "Hi there":
        #   print "aaaaaaaaaaaa"
        print message
        #exec message 
        