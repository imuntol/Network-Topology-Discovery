import socket
from socket import *
import thread
import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import json
import test_traffic as traffic
import test_mongoDB_done as topology

def connectDatabase(collectionsName):
    client = MongoClient()
    database = str(collectionsName)
    db = client['test']
    collection = db[database]
    return collection

collectionsName = "Thu26Nov2015_011006_traffic"
coll = connectDatabase(collectionsName)
count = coll.count()
a = []
for x in coll.find():
    a.append(x)
for d in a:
    del d['_id']
b = json.dumps(a)
c = json.loads(b)
print c
print c[0]['index']
print c[1]['index']
print c[2]['index']