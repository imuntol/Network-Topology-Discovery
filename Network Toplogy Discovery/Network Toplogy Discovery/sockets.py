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
test_word = ["s"]

while True:
    print "Waiting for Client to connnect"
    client,address = s.accept()
    print('connected from: ', address)
    #client.send(str.encode('Welcome to my Chat room!'))
    
    
    while True:
        #message = json.dumps({"cmd":"start","ip":"192.168.1.1","seed_ip":"192.168.1.2","com":"test"})
        message = client.recv(Buff_size)
        print message
        if not message:
            print "no message ----------------------------"
            break
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
            collectionsName = "Wed17Feb2016_053526"
            coll = connectDatabase(collectionsName)
            #count = coll.count()
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            print "wait 5 sec"
            time.sleep(5)
            print "sendind"
            data_topology_json = json.dumps(a)
            print data_topology_json
            client.send(data_topology_json)
            break
            

        elif message2['cmd'] == "traffic":
            print "ttttttttttttttttttttttttttttt"
            #indexTraffic = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)
            #collectionsName_traffic = str(collectionsName) + "_traffic_" + str(indexTraffic)
            collectionsName_traffic = "Wed17Feb2016_053526_traffic_0"
            coll = connectDatabase(collectionsName_traffic)
            #count = coll.count()
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            traffic_topology_json = json.dumps(a)
            print traffic_topology_json
            client.send(traffic_topology_json)
            print indexTraffic
            break
            #for x in coll.find():
            #    print x
        elif message2['cmd'] == "update_traffic":
            indexTraffic = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)
            print indexTraffic
            break
        else:
            print message2      