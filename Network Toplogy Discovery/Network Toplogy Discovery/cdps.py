import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
#import router as router
#import switch as switch

#community = "test"
#your_ip = "192.168.250.44"
#ip = "192.168.250.3"

#ip_r = ["192.168.250.2","192.168.250.3","192.168.250.1"]

SNMPv2MIB_sysName = ".1.3.6.1.2.1.1.5"

CISCOCDPMIB_cdpInterfaceName = ".1.3.6.1.4.1.9.9.23.1.1.1.1.6"

CISCOCDPMIB_cdpCacheDeviceId = ".1.3.6.1.4.1.9.9.23.1.2.1.1.6"
CISCOCDPMIB_cdpCacheDevicePort = ".1.3.6.1.4.1.9.9.23.1.2.1.1.7"

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

def New_reArrange_name(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("e.")[1];
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

def New_reArrange_cdpname(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("d.")[1];
        data[i] = data[i].split("=");
    numrows = len(data)    
    numcols = len(data[0])
    for i in range(0,numrows):
        for j in range(0,numcols):
            if j == 1:
                data[i][j] = data[i][j].split(":")[1].strip()
            else:
                data[i][j] = data[i][j].strip()
        data[i][0] = data[i][0].split(".")[0];
    return data

def New_reArrange_cdpinterface(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("t.")[1];
        data[i] = data[i].split("=");
    numrows = len(data)    
    numcols = len(data[0])
    for i in range(0,numrows):
        for j in range(0,numcols):
            if j == 1:
                data[i][j] = data[i][j].split(":")[1].strip()
            else:
                data[i][j] = data[i][j].strip()
        data[i][0] = data[i][0].split(".")[0];
    return data

def New_CDPs(name_data,interface_data,name_cdp,interface_cdp):
    #name_data = reArrange(getData(command(community,ip,SNMPv2MIB_sysName)))
    #interface_data = New_reArrange_name(getData(command(community,ip,CISCOCDPMIB_cdpInterfaceName)))
    #name_cdp = New_reArrange_cdpname(getData(command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
    #interface_cdp = New_reArrange_cdpinterface(getData(command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))

    #print name_data
    #print interface_data
    #print name_cdp
    #print interface_cdp
    #print name_cdp[0][0]
    #print interface_cdp[0][0]
    #print interface_data[0][0]
    newCDPs = [] 
    for i in range(0,len(name_cdp)):
        for j in range(0,len(interface_data)):
            if name_cdp[i][0] == interface_cdp[i][0] == interface_data[j][0]:
                #print interface_data[j][1]
                #print name_cdp[i][1]
                #print interface_cdp[i][1]
                #print "-----------------------------------"
                newCDPs.append(str(name_data[0]) + "," + interface_data[j][1] + "," + str(name_cdp[i][1]) + "," + str(interface_cdp[i][1]))

    #print newCDPs
    return newCDPs



#name_data = reArrange(getData(command(community,ip,SNMPv2MIB_sysName)))
#interface_data = New_reArrange_name(getData(command(community,ip,CISCOCDPMIB_cdpInterfaceName)))
#name_cdp = New_reArrange_cdpname(getData(command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
#interface_cdp = New_reArrange_cdpinterface(getData(command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))

#print name_data
#print interface_data
#print name_cdp
#print interface_cdp