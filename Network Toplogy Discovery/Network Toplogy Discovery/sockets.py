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
import thread
import anaysitData as an


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

def update_traffic(community,ipTraffic,collectionsName,indexTraffic,config_name):
    indexTraffic,traffic_datetime = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)   #Wed17Feb2016_053526
    collectionsNameTopo = collectionsName
    collectionsNameTraff = collectionsName+"_traffic_"+indexTraffic
    aaa,collectionsName_traffic_new = an.anaysit(collectionsNameTopo,collectionsNameTraff,indexTraffic)
    ##topo_config_name
    coll_config = connectDatabase(config_name)
    coll_config.update({"index":"0"},{'$set':{"traffic_index":str(indexTraffic)}})
    ##
    ##traffic_config_name
    config_traffic_name = "timeline_"+collectionsName_traffic_new
    coll_config_traffic = connectDatabase(config_traffic_name)
    coll_config_traffic.insert_one({"index":"0"})
    coll_config_traffic.update({"index":"0"},{'$set':{"name":collectionsName_traffic_new,"date_time":traffic_datetime}})
    ##

    return indexTraffic,collectionsName_traffic_new


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
        print "1:" + str(message) + str(len(message))
        if len(message) == 0:
            sys.exit(0)
        if message[0] != '{': #and message[0] != '['
            continue
        message = json.loads(message)
        print "2:" + str(message)
        if message['cmd'] == "start":
            ip = message['ip']
            seed_ip = message['seed_ip']
            community = message['com']
            username = message['username']
            password = message['compassword']
            indexTraffic = 0
            community,ipTraffic,collectionsName,config_name = topo.topology(ip,seed_ip,community,username,password)
            
            #collectionsName = "Sun13Mar2016_163108"
            #collectionsName = "Mon18Apr2016_225902"
            coll = connectDatabase(collectionsName)
            #count = coll.count()
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
 
            data_topology_json = json.dumps(a)
            a = []
            a.append(data_topology_json)
            name = makeFile("data")
            writeFile(a,name)


            indexTraffic,collectionsName_traffic_new = update_traffic(community,ipTraffic,collectionsName,indexTraffic,config_name)
            ### traffic
            #indexTraffic = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)   #Wed17Feb2016_053526
           
            #collectionsNameTopo = collectionsName
            #collectionsNameTraff = collectionsName+"_traffic_"+indexTraffic
            #aaa,collectionsName_traffic_new = an.anaysit(collectionsNameTopo,collectionsNameTraff,indexTraffic)
            ##config_name
            #coll_config = connectDatabase(config_name)
            #coll_config.update({"index":"0"},{'$set':{"traffic_index":str(indexTraffic)}})
            ###
            client.send("done")
                 
        elif message['cmd'] == "traffic":
            coll = connectDatabase(collectionsName_traffic_new)
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            traffic_topology_json = json.dumps(a)
            a = []
            a.append(data_topology_json)
            name = makeFile("traffic")
            writeFile(a,name)
            client.send("done")
  
        elif message['cmd'] == "update_traffic":
            #collectionsName_traffic = str(collectionsName) + "_traffic_" + str(indexTraffic)  # Wed17Feb2016_053526_traffic_0
            #coll = connectDatabase(collectionsName_traffic)
            try:
               thread.start_new_thread( update_traffic, (community,ipTraffic,collectionsName,indexTraffic,config_name) )

            except:
               print "Error: unable to start thread"

        elif message['cmd'] == "save":
            location = []
            for temp in message['location']:
                location.append(temp)
            #collectionsName = "Mon18Apr2016_225902"
            coll = connectDatabase(collectionsName)
            for i in range(0,len(location)):
                coll.update({"index":str(i)},{'$set':{"location":location[i]}})
            
            #config_name
            coll_config = connectDatabase(config_name)
            coll_config.update({"index":"0"},{'$set':{"name":message['name']}})
         
        elif message['cmd'] == "load":
            client = MongoClient('localhost',27017)
            db = client['test']
            data = db.collection_names()
            temp = []
            for i in data:
                if "_config" in i:
                    #print i
                    temp.append(i)
            a=[]
            for i in range(0,len(temp)):
                 #print temp[i]
                 a.append(str(temp[i]))
            b=[]
            for i in a:
                coll = connectDatabase(i)
                b.append(coll.find_one('name'))
            c=[]
            for i in range(0,len(a)):
                c.append(str(a[i])+","+str(b[i]))
            #print c

            name = makeFile_txt("list_save")
            writeFile(c,name)
            client.send("done")

        elif message['cmd'] == "select":
            config_name = message['config_name']
            coll_config = connectDatabase(config_name)
            data = coll_config.find_one()
            indexTraffic = data['traffic_index']



            collectionsName = config_name.split("_config")[0];
            coll = connectDatabase(collectionsName)
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']

            data_topology_json = json.dumps(a)
            a = []
            a.append(data_topology_json)
            name = makeFile("data")
            writeFile(a,name)
            client.send("done")

        elif message['cmd'] == "timeline":
            client = MongoClient('localhost',27017)
            db = client['test']
            data = db.collection_names()
            temp = []
            for i in data:
                if "timeline_"+collectionsName in i:
                    #print i
                    temp.append(i)
            a=[]
            for i in range(0,len(temp)):
                 #print temp[i]
                 a.append(str(temp[i]))
            b=[]
            for i in a:
                coll_timeline = connectDatabase(i)
                b.append(coll_timeline.find_one('name')+","+coll_timeline.find_one('date_time'))
            name = makeFile_txt("timeline")
            writeFile(b,name)
            client.send("done")

        elif message['cmd'] == "stimeline":
            db_timeline = message['db_timeline']
            coll_timeline = connectDatabase(db_timeline)
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                del d['_id']
            traffic_topology_json = json.dumps(a)
            a = []
            a.append(data_topology_json)
            name = makeFile("traffic")
            writeFile(a,name)

        else:
            print message