import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import test_traffic as traffic
import test_mongoDB_done as topology
#ipTraffic = ['192.168.1.2', '192.168.2.2', '192.168.4.2', '192.168.3.2', '192.168.5.2']
#community = "test"
#databaseName = "abcd"


community,ipTraffic,collectionsName = topology.topology("192.168.1.1","192.168.1.2","test")
traffic.traffic(community,ipTraffic,collectionsName)