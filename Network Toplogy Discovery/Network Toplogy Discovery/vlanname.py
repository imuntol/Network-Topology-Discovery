import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import router as router


#community = "test"
#your_ip = "192.168.250.44"
#ip = "192.168.250.1"

def New_reArrange(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("1.")[1];
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

CISCOVTPMIB_vtpVlanName = "1.3.6.1.4.1.9.9.46.1.3.1.1.4"

#vtp_vlanname = vn.New_reArrange(router.getData(router.command(community,ip,CISCOVTPMIB_vtpVlanName)))

def vlanname(vtp_vlanname):
    vlan_name = []
    for i in range(0,len(vtp_vlanname)):
        vlan_name.append("vlan" + str(vtp_vlanname[i][0]) + "," + str(vtp_vlanname[i][1]))
    return vlan_name