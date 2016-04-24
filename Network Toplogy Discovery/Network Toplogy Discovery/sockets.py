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
import ast


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
    clients = MongoClient()
    database = str(collectionsName)
    db = clients['test']
    collection = db[database]
    return collection

def update_traffic(community,ipTraffic,collectionsName,indexTraffic,config_name):
    print "indexTraffic(update_traffic1) : " + str(indexTraffic)
    indexTraffic,traffic_datetime = traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)   #Wed17Feb2016_053526
    print "indexTraffic(update_traffic2) : " + str(indexTraffic)
    collectionsNameTopo = collectionsName
    collectionsNameTraff = str(collectionsName)+"_traffic_"+str(indexTraffic-1)
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


indexTraffic = 0
Host = "localhost"
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
            password = message['password']
            
            community,ipTraffic,collectionsName,config_name = topo.topology(ip,seed_ip,community,username,password)
            
            print "ip traffic(start) : " + str(ipTraffic)
            print "indexTraffic(start) : " + str(indexTraffic)
            #config_name
            coll_config = connectDatabase(config_name)
            coll_config.update({"index":"0"},{'$set':{"ip_traffic":str(ipTraffic)}})
            coll_config.update({"index":"0"},{'$set':{"community":str(community)}})
            coll = connectDatabase(collectionsName)
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                try:
                    del d['_id']
                except:
                    pass
 
            data_topology_json = json.dumps(a)
            a = []
            a.append(data_topology_json)
            name = makeFile("data")
            writeFile(a,name)
            indexTraffic,collectionsName_traffic_new = update_traffic(community,ipTraffic,collectionsName,indexTraffic,config_name)
            
            print "collectionsName_traffic_new : " + str(collectionsName_traffic_new)
            client.send("done")
                 
        elif message['cmd'] == "traffic":
            print "indexTraffic(traffic) : " + str(indexTraffic)
            coll = connectDatabase(collectionsName_traffic_new)
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                try:
                    del d['_id']
                except:
                    pass
            #print "data traffic : " + str(a)
            traffic_topology_json = json.dumps(a)
            a = []
            a.append(traffic_topology_json)
            name = makeFile("traffic")
            writeFile(a,name)
            client.send("done")
  
        elif message['cmd'] == "update_traffic":
            data = coll_config.find_one()
            indexTraffic = data['traffic_index']
            try:
               thread.start_new_thread(update_traffic,(community,ipTraffic,collectionsName,indexTraffic,config_name))

            except Exception,e:
                print e

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
            coll_config.update({"index":"0"},{'$set':{"name":message['topoName']}})
         
        elif message['cmd'] == "load":
            clients = MongoClient('localhost',27017)
            db = clients['test']
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
                b.append(coll.find_one())
                for j in b:
                    try:
                        del j['_id']
                    except:
                        pass
            c=[]
            for k in range(0,len(b)):
                if b[k]['name'] == "none":
                    pass
                else:
                    c.append(str(a[k])+","+str(b[k]['name']))

            name = makeFile_txt("list_save")
            writeFile(c,name)
            client.send("done")

        elif message['cmd'] == "select":
            ipTraffic = []
            config_name = message['config_name']
            coll_config = connectDatabase(config_name)
            data = coll_config.find_one()
            indexTraffic = data['traffic_index']
            community = data['community']
            a = data['ip_traffic']
            n = ast.literal_eval(a)
            for i in range(0,len(n)):
                ipTraffic.append(n[i])

            collectionsName = config_name.split("_config")[0];
            collectionsName_traffic_new = str(collectionsName)+"_traffic_"+str(int(indexTraffic)-1)+"_new"
            coll = connectDatabase(collectionsName)

            print "community(select) : " + str(community)
            print "ipTraffic(select) : " + str(ipTraffic)
            print "indexTraffic(select) : " + str(indexTraffic)
            print "collectionsName(select) : " + str(collectionsName)
            print "config_name(select) : " + str(config_name)
            a = []
            for x in coll.find():
                a.append(x)
            for d in a:
                try:
                    del d['_id']
                except:
                    pass

            data_topology_json = json.dumps(a)
            a = []
            a.append(data_topology_json)
            name = makeFile("data")
            writeFile(a,name)
            client.send("done")

        elif message['cmd'] == "timeline":
            clients = MongoClient('localhost',27017)
            db = clients['test']
            data = db.collection_names()
            temp = []
            for i in data:
                if "timeline_"+str(collectionsName) in i:
                    temp.append(i)
            a=[]
            for i in range(0,len(temp)):
                    a.append(str(temp[i]))
            b=[]
            for i in a:
                coll_timeline = connectDatabase(i)
                b.append(coll_timeline.find_one())
                for j in b:
                    try:
                        del j['_id']
                    except:
                        pass
            c = []
            for i in range(0,len(b)):
                c.append(str(b[i]["name"])+","+str(b[i]["date_time"]))

            name = makeFile_txt("timeline")
            writeFile(c,name)
            client.send("done")

        elif message['cmd'] == "stimeline":
            db_timeline = message['db_timeline']
            coll_timeline = connectDatabase(db_timeline)
            traffic_topology_json = []
            a = []
            for x in coll_timeline.find():
                a.append(x)
            for d in a:
                try:
                    del d['_id']
                except:
                    pass
            traffic_topology_json = json.dumps(a)
            print traffic_topology_json
            a = []
            a.append(traffic_topology_json)
            name = makeFile("traffic")
            writeFile(a,name)
            time.sleep(0.5)
            print "w8 0.5 sec"
            client.send("done")
            print "sended"

        else:
            print message