import socket
from socket import *
import sys
import os
import pymongo
from pymongo import MongoClient
from pymongo import *
import datetime
from datetime import datetime
import time
import json
import numpy
import anaysitData as an
import unicodedata

def makeFile(filename):
    directory = "json"
    filename = filename + ".json"
    if not os.path.exists(directory):
            os.makedirs(directory)
    thefile = open("json/"+str(filename),'w')
    thefile.close()
    return filename

def makeFile_txt(filename):
    directory = "json"
    filename = filename + ".txt"
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
Host = "192.168.173.1"
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
    while(True):
        try:
            message = client.recv(Buff_size)
        except:
            #sys.exit(0)
            break
        print "1: " + str(message)+" " + str(len(message))
        if len(message) == 0:
            #sys.exit(0)
            break
        if message[0] != '{': #and message[0] != '['
            continue
        message = json.loads(message)
        print "2: " + str(message)
        
        if message['cmd'] == "start":
            ip = message['ip']
            #seed_ip = message['seed_ip']
            #community = message['com']
            #username = message['username']
            #password = message['compassword']
            #community,ipTraffic,collectionsName,config_name = topo.topology(ip,seed_ip,community,username,password)
            
            ##collectionsName = "Sun13Mar2016_163108"
            ##collectionsName = "Mon18Apr2016_225902"
            #coll = connectDatabase(collectionsName)
            ##count = coll.count()
            #a = []
            #for x in coll.find():
            #    a.append(x)
            #for d in a:
            #    del d['_id']
 
            #data_topology_json = json.dumps(a)
            #a = []
            #a.append(data_topology_json)
            #name = makeFile("data")
            #writeFile(a,name)
            ### traffic
            #indexTraffic = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)   #Wed17Feb2016_053526
           
            #collectionsNameTopo = collectionsName
            #collectionsNameTraff = collectionsName+"_traffic_"+indexTraffic
            #aaa,collectionsName_traffic_new = an.anaysit(collectionsNameTopo,collectionsNameTraff,indexTraffic)
            ##config_name
            #coll_config = connectDatabase(config_name)
            #coll_config.update({"index":"0"},{'$set':{"traffic_index":str(indexTraffic)}})

            time.sleep(2)
            print "w8 2 sec"
            client.send("done")
            print "sended"

        elif message['cmd'] == "traffic":
            #coll = connectDatabase(collectionsName_traffic_new)
            #a = []
            #for x in coll.find():
            #    a.append(x)
            #for d in a:
            #    del d['_id']
            #traffic_topology_json = json.dumps(a)
            #a = []
            #a.append(data_topology_json)
            #name = makeFile("traffic")
            #writeFile(a,name)

            time.sleep(2)
            print "w8 2 sec"
            client.send("done")
            print "sended"

        elif message['cmd'] == "load":
            #client = MongoClient('localhost',27017)
            #db = client['test']
            #data = db.collection_names()
            #temp = []
            #for i in data:
            #    if "_config" in i:
            #        #print i
            #        temp.append(i)
            #a=[]
            #for i in range(0,len(temp)):
            #     #print temp[i]
            #     a.append(str(temp[i]))
            #b=[]
            #for i in a:
            #    coll = connectDatabase(i)
            #    b.append(coll.find_one('name'))
            #c=[]
            #for i in range(0,len(a)):
            #    c.append(str(a[i])+","+str(b[i]))
            #print c

            #name = makeFile_txt("list_save")
            #writeFile(c,name)
            time.sleep(2)
            print "w8 2 sec"
            client.send("done")
            print "sended"
        
        elif message['cmd'] == "select":
            config_name = message['config_name']
            print config_name
            #coll_config = connectDatabase(config_name)
            #data = coll_config.find_one()
            #indexTraffic = data['traffic_index']



            #collectionsName = config_name.split("_config")[0];
            #coll = connectDatabase(collectionsName)
            #a = []
            #for x in coll.find():
            #    a.append(x)
            #for d in a:
            #    del d['_id']

            #data_topology_json = json.dumps(a)
            #a = []
            #a.append(data_topology_json)
            #name = makeFile("data")
            #writeFile(a,name)
            time.sleep(2)
            print "w8 2 sec"
            client.send("done")
            print "sended"

        else:
            print message



#collectionsName = "Mon18Apr2016_225902"
#coll = connectDatabase(collectionsName)

### test config
##config_name = "asdasdd_test_config_3"
##coll_config = connectDatabase(config_name)
##coll_config.insert_one({"name":"none","date":"asdasdsad","index":"0","traffic_index":"0"})
##coll_config.update({"index":"0"},{'$set':{"name":"test1"}})
###

    #client = MongoClient('localhost',27017)
    #db = client['test']
    #data = db.collection_names()
    #temp = []
    #for i in data:
    #    if "_config" in i:
    #        #print i
    #        temp.append(i)
    #a=[]
    #for i in range(0,len(temp)):
    #     #print temp[i]
    #     a.append(str(temp[i]))
    #b=[]
    #for i in a:
    #    coll = connectDatabase(i)
    #    b.append(coll.find_one('name'))
    #c=[]
    #for i in range(0,len(a)):
    #    c.append(str(a[i])+","+str(b[i]))
    #print c
    #for i in c:
    #    print i.split("_config")[0];

    #name = makeFile_txt("savesave")
    #writeFile(c,name)

#coll = connectDatabase("asdasdd_test_config_3")
#data = coll.find_one()
#a = data['traffic_index']
#print a