import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time

#community = "test"
#your_ip = "192.168.1.1"
#ip = "192.168.1.2"

### OID ###
IPMIB_ipAdEntAddr = ".1.3.6.1.2.1.4.20.1.1"
IPMIB_ipAdEntIfIndex = ".1.3.6.1.2.1.4.20.1.2"
IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
IPMIB_ipAdEntNetMask = ".1.3.6.1.2.1.4.20.1.3"
###########

def command(community,ip,oid):
    command = "snmpwalk -v 2c -c" + " " + community + " " + ip + " " + oid
    return command

def getData(command):
    data = (os.popen(command).read())
    data = data.split("\n",)
    data = [x for x in data if x != '']
    for i in range(0,len(data)):
        data[i] = data[i].strip()
    #print data
    #Output -> list
    return data

def detail(data):
    if data == []:
        print "not router or switch"
    else:
        data[0] = data[0].split("G:")[1];
        data[0] = data[0].strip()
        temp = ""
        for i in range(0,len(data)):
            temp = temp + data[i]
        data = []
        data.append(temp)
        #print data
    return data

def reArrange(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("=")[1];
        data[i] = data[i].split(":")[1];
        data[i] = data[i].split(" ")[1];
    #print data
    return data

def New_reArrange(data):
    for i in range(0,len(data)):
        data[i] = data[i].split(".")[1];
        data[i] = data[i].split("=");
    numrows = len(data)    
    numcols = len(data[0])
    for i in range(0,numrows):
        for j in range(0,numcols):
            if j == 1:
                data[i][j] = data[i][j].split(":")[1].strip()
            else:
                data[i][j] = data[i][j].strip()
    return data

def getRowCol(data):
    numrows = len(data)    
    numcols = len(data[0])
    return numrows,numcols

#ip_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntAddr)))
#subnet_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntNetMask)))
#index_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntIfIndex)))
#interface_data = New_reArrange(getData(command(community,ip,IFMIB_ifDescr)))

#print "ip : " + str(ip_data)
#print "subnet : " + str(subnet_data)
#print "index : " + str(index_data)
#print "data : " + str(interface_data)

def interfacedetail(ip_data,subnet_data,index_data,interface_data):
    r,c = getRowCol(ip_data)
    rr,cc = getRowCol(interface_data)

    newData = []
    for i in range(0,r):
        for j in range(0,rr):
            if index_data[i] == interface_data[j][0]:
                newData.append(str(ip_data[i]) + "," + str(subnet_data[i]) + "," + str(interface_data[j][1]))
    #print newData
    return newData