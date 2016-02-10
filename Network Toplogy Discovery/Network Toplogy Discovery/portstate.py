import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
#import router as router
#import test_switch as switch
#import check_device as check
#import topology as topo
#import numpy as np

community = "test"
your_ip = "192.168.250.50"
ip = "192.168.250.1"

### OID ###

IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
BRIDGEMIB_dot1dStpPort = "1.3.6.1.2.1.17.2.15.1.1" #stp port
BRIDGEMIB_dot1dStpPortState = ".1.3.6.1.2.1.17.2.15.1.3" #stp port state
BRIDGEMIB_dot1dBasePortIfIndex = ".1.3.6.1.2.1.17.1.4.1.2" # port index

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

def reArrange(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("=")[1];
        if data[0] == " No Such Instance currently exists at this OID":
            pass
        else:
            data[i] = data[i].split(":")[1];
            data[i] = data[i].split(" ")[1];
    #print data
    return data

def getRowCol(data):
    numrows = len(data)    
    numcols = len(data[0])
    return numrows,numcols

def portState(stp_port,stp_portstate,stp_portindex,interface_data):

    #print stp_port
    #print stp_portstate
    #print stp_portindex
    #print interface_data
    #print "----------------------------------------------"
    interface_state = []
    if stp_port == [" No Such Instance currently exists at this OID"]:
        interface_state.append("No Vlan Default")
    else:
        
        r,c = getRowCol(stp_port)
        ro,co = getRowCol(stp_portindex)
        row,col = getRowCol(interface_data)

        for i in range(0,r):
             for j in range(0,ro):
                 if stp_port[i] == stp_portindex[j][0]:
                     index = stp_portindex[j][1]
                     #print index
                     for k in range(0,row):
                         if index == interface_data[k][0]:
                            interface_state.append(str(interface_data[k][1]) + "," + str(stp_portstate[i][1]))
        #print "----------------------------------------------"
    return interface_state









#stp_port = reArrange(getData(command(community,ip,BRIDGEMIB_dot1dStpPort)))
#stp_portstate = New_reArrange(getData(command(community,ip,BRIDGEMIB_dot1dStpPortState)))
#stp_portindex = New_reArrange(getData(command(community,ip,BRIDGEMIB_dot1dBasePortIfIndex)))
#interface_data = New_reArrange(getData(command(community,ip,IFMIB_ifDescr)))                 

#a = portState(stp_port,stp_portstate,stp_portindex,interface_data)    
#print a
#print interface_state
                   