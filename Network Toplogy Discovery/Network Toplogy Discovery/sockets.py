import socket
from socket import *
#socket.gethostbyname
#import thread
import sys
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


def makeFile(filename):
    directory = "json"
    filename = filename + ".json"
    if not os.path.exists(directory):
            os.makedirs(directory)
    thefile = open("json/"+str(filename),'w')
    thefile.close()
    return filename

def writeFile(data,filename):
    #directory = "result"
    #filename = datetime.now()
    ### path ###
    #if not os.path.exists(directory):
    #    os.makedirs(directory)
    ############
    thefile = open("json/"+filename,'a')
    for item in data:
        thefile.write("%s\n" % item)
    thefile.close()

def connectDatabase(collectionsName):
    client = MongoClient()
    database = str(collectionsName)
    db = client['test']
    collection = db[database]
    return collection


a = []
#Client = "192.168.1.22"
#Client_port = 50001
Host = "10.20.23.18"
Port = 50000
Buff_size = 1024

#server
s = socket(AF_INET, SOCK_STREAM) 
s.bind((Host,Port))
s.listen(1)


indexTraffic = 0

while True:
    print "Waiting for Client to connnect"
    client,address = s.accept()
    print('connected from: ', address)
    print('client from: ', client)
    print('s from: ', s)
    
    #client.send(str.encode('Welcome to my Chat room!'))
    #message = json.dumps({"cmd":"start","ip":"192.168.1.1","seed_ip":"192.168.1.2","com":"test"})
    
    while(True):
        try:
            message = client.recv(Buff_size)
        except:
            sys.exit(0)
        #if s is None:
        #    print 'could not open socket'
        #    sys.exit(1)
        print "1:" + str(message) + str(len(message))
        if len(message) == 0:
            sys.exit(0)
        if message[0] != '{': #and message[0] != '['
            continue
        message = json.loads(message)
        print "2:" + str(message)
        if message['cmd'] == "start":
            ip = message['ip']
            #print ip
            seed_ip = message['seed_ip']
            #print seed_ip
            community = message['com']
            #print community
            #username = message2['username']
            #password = message2['compassword']

            #community,ipTraffic,collectionsName = topo.topology(ip,seed_ip,community,username,password)
            
            #collectionsName = "Sun13Mar2016_163108"
            collectionsName = "Mon18Apr2016_225902"
            coll = connectDatabase(collectionsName)
            #count = coll.count()
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            print "wait 1 sec"
            time.sleep(1)
            print "sendind"

            data_topology_json = json.dumps(a)
            a = []
            a.append(data_topology_json)
            name = makeFile("jjjjjj")
            writeFile(a,name)
            print data_topology_json
           
            #client.send(data_topology_json)
            #indexTraffic = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)   #Wed17Feb2016_053526
            
        elif message['cmd'] == "traffic":
            print "ttttttttttttttttttttttttttttt"
            #indexTraffic = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)
            ##collectionsName_traffic = str(collectionsName) + "_traffic_" + str(indexTraffic)   Wed17Feb2016_053526_traffic_0

            #collectionsNameTopo = collectionsName
            #collectionsNameTraff = collectionsName+"_traffic_"+indexTraffic
            #aaa = an.anaysit(collectionsNameTopo,collectionsNameTraff)
            #collectionsName_traffic_new = collectionsName+"_traffic_new"+indexTraffic

            collectionsName_traffic = "Wed17Feb2016_053526_traffic_0" #use collectionsName_traffic_new instead
            coll = connectDatabase(collectionsName_traffic)
            #count = coll.count()
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            traffic_topology_json = json.dumps(a)
            #print traffic_topology_json
            client.send(traffic_topology_json)
            #print indexTraffic
            
            #for x in coll.find():
            #    print x
        elif message['cmd'] == "update_traffic":
            collectionsName_traffic = str(collectionsName) + "_traffic_" + str(indexTraffic)  # Wed17Feb2016_053526_traffic_0
            coll = connectDatabase(collectionsName_traffic)
            #count = coll.count()
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            traffic_topology_json = json.dumps(a)
            #print traffic_topology_json
            client.send(traffic_topology_json)

        elif message['cmd'] == "save":
            location = []
            for temp in message['location']:
                location.append(temp)
            collectionsName = "Mon18Apr2016_225902"
            coll = connectDatabase(collectionsName)
            for i in range(0,len(location)):
                coll.update({"index":str(i)},{'$set':{"location":location[i]}})
        else:
            print message