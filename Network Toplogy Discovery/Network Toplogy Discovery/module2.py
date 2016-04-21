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

def connectDatabase(collectionsName):
    clients = MongoClient()
    database = str(collectionsName)
    db = clients['test']
    collection = db[database]
    return collection

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

def timeline():
    collectionsName = "Thu21Apr2016_210459"
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
        for i in b:
            del i['_id']
    c = []
    for i in range(0,len(b)):
        #print b[i]["name"]
        c.append(str(b[i]["name"])+","+str(b[i]["date_time"]))

    name = makeFile_txt("timeline")
    writeFile(c,name)

def load():
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
    print c
    name = makeFile_txt("list_save")
    writeFile(c,name)
    client.send("done")


def Hi():
    #time.sleep(1)
    print "adsadsa"
    

#for j in range(0,10):
#    try:
#        thread.start_new_thread(Hi,())
        
#    except:
#        print "Error: unable to start thread"


#ipTraffic = []
#config_name = "Fri22Apr2016_011710_config"
#coll_config = connectDatabase(config_name)
#data = coll_config.find_one()
##indexTraffic = data['traffic_index']
##community = data['community']
#print type(data['ip_traffic'])
#a = data['ip_traffic']
#n = ast.literal_eval(a)
#for i in range(0,len(n)):
#    #print n[i]
#    ipTraffic.append(n[i])
#print ipTraffic[1]
##print n[1]


