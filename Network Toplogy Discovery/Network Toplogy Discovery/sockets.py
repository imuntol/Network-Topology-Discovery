import socket
from socket import *
#socket.gethostbyname
import thread
import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import json
import test_traffic as traffic
import router as router
import switch as switch
import check_device as check
import topology as topo



def connectDatabase(collectionsName):
    client = MongoClient()
    database = str(collectionsName)
    db = client['test']
    collection = db[database]
    return collection


a = []
Client = "10.20.21.194"
Client_port = 50001
Host = "10.20.21.84"
Port = 50000
Buff_size = 1024

#server
s = socket(AF_INET, SOCK_STREAM) 
s.bind((Host,Port))
s.listen(1)


indexTraffic = 0

#state = True
#while(state):
#	print "What are you thinking ?"
#	a = raw_input("Input : ")
#	print "Output : " + str(a)
#	if a == "exit":
#		state = False
#client
#sc = socket(AF_INET, SOCK_STREAM)
#sc.connect((Client,Client_port))


while True:
    print "Waiting for Client to connnect"
    client,address = s.accept()
    print('connected from: ', address)
    #client.send(str.encode('Welcome to my Chat room!'))
    
    index = 1
    while True:
        #message = json.dumps({"cmd":"start","ip":"192.168.1.1","seed_ip":"192.168.1.2","com":"test"})
        message = client.recv(Buff_size)
        if not message:
            break
        #print message
        #print coll.count()
        message2 = json.loads(message)
        if message2['cmd'] == "start":
            ip = message2['ip']
            print ip
            seed_ip = message2['seed_ip']
            print seed_ip
            community = message2['com']
            print community
            #community,ipTraffic,collectionsName = topo.topology(your_ip,ip,community)
            #indexTraffic = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)
            collectionsName = "Thu11Feb2016_214109"
            coll = connectDatabase(collectionsName)
            #count = coll.count()
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            print "wait 3 sec"
            time.sleep(3)
            print "sendind"
            data_topology_json = json.dumps(a)
            print data_topology_json
            client.send(data_topology_json)

        elif message2['cmd'] == "traffic":
            collectionsName = collectionsName +"_"+ str(index)
            traffic.traffic(community,ipTraffic,collectionsName)

            coll = connectDatabase(collectionsName+"_traffic")
            #count = coll.count()
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            traffic_topology_json = json.dumps(a)
            print traffic_topology_json
            client.send(traffic_topology_json)
            index += 1
            #for x in coll.find():
            #    print x
        else:
            print message2      