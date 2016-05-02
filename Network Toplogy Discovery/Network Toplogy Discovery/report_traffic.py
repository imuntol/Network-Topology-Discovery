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

ip = "192.168.1.2"
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

    
    #print In2

    In = float(In2[2][1]) - float(In1[2][1])
    Out = float(Out2[2][1]) - float(Out1[2][1])

    #print In*8
    #print Out*8

    In =  round(In*8/(t*1024*1024),5)
    Out =  round(Out*8/(t*1024*1024),5)

    #In = round(((float(trafficIn_2[i][1])*8) - (float(trafficIn_1[i][1])*8))/(1024*1024),2)
    #Out = round(((float(trafficOut_2[i][1])*8) - (float(trafficOut_1[i][1])*8))/(1024*1024),2)
                
    print "In : " + str(In) +" Mb/s"
    print "Out : " + str(Out) +" Mb/s"
    print "total : " + str(In+Out) +" Mb/s"
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