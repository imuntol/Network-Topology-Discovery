import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time

community = "test"
your_ip = "192.168.200.33"
ip = "192.168.200.2"

### OID ###
IPMIB_ipAdEntAddr = ".1.3.6.1.2.1.4.20.1.1" #ip
IPMIB_ipNetToMediaNetAddress = ".1.3.6.1.2.1.4.22.1.3" #ip+ip cdp
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


#ip_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntAddr)))
#ip_cdp = reArrange(getData(command(community,ip,IPMIB_ipNetToMediaNetAddress)))

#done_list = []
#notdone_list = []

def findlist(ip_data,ip_cdp,done_list,notdone_list):
    #done_list.append(your_ip)
    #for i in range(0,len(ip_data)):
    #    done_list.append(ip_data[i])

    #print "before done list : " + str(done_list)
    #print "before ip cdpe : " + str(ip_cdp)
    #print "before notdone list : " + str(notdone_list)

    ## check ip that already get data
    for j in range(0,len(done_list)):
        if done_list[j] in ip_cdp:
            ip_cdp.remove(str(done_list[j]))
            

    #print "###################################################"


    ## make list for ip that didnt get data yet
    for j in range(0,len(notdone_list)):
        if notdone_list[j] in ip_cdp:
            ip_cdp.remove(str(notdone_list[j]))
    for k in range(0,len(ip_cdp)):
        notdone_list.append(ip_cdp[k])

    #print "after done list : " + str(done_list)
    #print "after ip cdpe : " + str(ip_cdp)
    #print "after notdone list : " + str(notdone_list)
    return done_list,notdone_list