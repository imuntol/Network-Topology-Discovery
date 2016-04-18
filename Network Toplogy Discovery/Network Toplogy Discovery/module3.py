import socket
from socket import *
import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import json
import numpy
import anaysitData as an

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

#collectionsNameTopo = "Sun13Mar2016_163108"
#collectionsNameTraff = "Sun13Mar2016_163108_traffic_0"
#aaa = an.anaysit(collectionsNameTopo,collectionsNameTraff)
#print aaa
collectionsName = "Mon18Apr2016_225902"
coll = connectDatabase(collectionsName)
count = coll.count()
a = []
for x in coll.find():
    a.append(x)
for d in a:
    del d['_id']
b = json.dumps(a)
c = json.loads(b)
print b
temp = []
temp.append(b)
name = makeFile(collectionsName)
writeFile(temp,name)