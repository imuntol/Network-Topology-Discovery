import socket
from socket import *
import json
import sys

a = []
#Client = "192.168.1.22"
#Client_port = 50001
Host = "10.20.22.90"
Port = 50000
Buff_size = 1024

s = socket(AF_INET, SOCK_STREAM) 
s.bind((Host,Port))
s.listen(1)

while True:
    print "Waiting for Client to connnect"
    client,address = s.accept()
    print('connected from: ', address)
    print('client from: ', client)
    print('s from: ', s)
    
    #client.send(str.encode('Welcome to my Chat room!'))

    #message = json.dumps({"cmd":"start","ip":"192.168.1.1","seed_ip":"192.168.1.2","com":"test"})
    print "w8 cmd"
    while(True):
        try:
            message = client.recv(Buff_size)
        except:
            sys.exit(0)
        print "1 " + str(message)
        if message[0] != '{' : #and message[0] != '['
            continue
        message = json.loads(message)
        print "2 " + str(message)
