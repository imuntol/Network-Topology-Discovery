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

ip = "192.168.200.1"
community = "test"
time_ = []
traffic_ = []
a = 0
while(a<=25):
    print "----------------------------------- " +str(a)+ "--------------------------"
    date_time = datetime.now()
    start_time = time.time()
    In1 = traffic.traffIn(community,ip)
    Out1 = traffic.traffIn(community,ip)
    time.sleep(20)
    In2 = traffic.traffIn(community,ip)
    Out2 = traffic.traffIn(community,ip)
    stop_time = time.time()
    ifSpeed = traffic.ifSpeed(community,ip)
    t = (stop_time-start_time)

    print date_time.strftime('%a%d%b%Y_%H:%M:%S')
    #print start_time
    #print stop_time
    #print t

    #print "In1 : " + str(In1[25][1])
    #print "In2 : " + str(In2[25][1])
    #print "BW : " + str(ifSpeed[25][1])

    In = ((int(In2[25][1]) - int(In1[25][1])))/(t*1024)
    Out = ((int(Out2[25][1]) - int(Out1[25][1])))/(t*1024)
    print "In : " + str(In)
    print "Out : " + str(Out)
    print "total : " + str(In+Out)
    time_.append(date_time)
    traffic_.append(str(In+Out))
    a+=1

directory = "json"
filename1 = "mytraffic.txt"
if not os.path.exists(directory):
        os.makedirs(directory)
thefile = open("json/"+str(filename1),'w')
thefile.close()

thefile = open("json/"+filename1,'a')
for item in traffic_:
    thefile.write("%s\n" % item)
thefile.close()



filename2 = "mytraffic_time.txt"
if not os.path.exists(directory):
        os.makedirs(directory)
thefile = open("json/"+str(filename2),'w')
thefile.close()

thefile = open("json/"+filename2,'a')
for item in time_:
    thefile.write("%s\n" % item)
thefile.close()