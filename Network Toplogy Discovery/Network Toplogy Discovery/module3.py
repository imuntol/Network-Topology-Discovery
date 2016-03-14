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

def connectDatabase(collectionsName):
    client = MongoClient()
    database = str(collectionsName)
    db = client['test']
    collection = db[database]
    return collection

collectionsNameTopo = "Sun13Mar2016_163108"
collectionsNameTraff = "Sun13Mar2016_163108_traffic_0"
aaa = an.anaysit(collectionsNameTopo,collectionsNameTraff)
#print aaa
collectionsName = "Sun13Mar2016_163108_traffic_new"
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