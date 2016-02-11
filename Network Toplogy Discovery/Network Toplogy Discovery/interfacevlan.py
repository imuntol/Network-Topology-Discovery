import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import router as router
#import test_switch as switch
#import check_device as check
#import topology as topo

#community = "test"
#your_ip = "192.168.250.50"
#ip = "192.168.250.1"

### OID ###

IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2" #interface
CISCOSMI_ciscoMgmt = ".1.3.6.1.4.1.9.9.68.1.2.2.1.2" # vlan interface
CISCOVTPMIB_vlanTrunkPortDynamicStatus = ".1.3.6.1.4.1.9.9.46.1.6.1.1.14" # check trunk port


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

def New_reArrange_vlan(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("CISCO-SMI::ciscoMgmt.68.1.2.2.1.2.")[1];
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
    #print numrows
    #print numcols
    return numrows,numcols

def interfaceVlan(interface_data,trunk,vlan_interface):
    
    #print trunk
    #print interface_data
    new_trunk = [i for i in trunk if "trunking(1)" in i]
    #print new_trunk
    #print new_trunk
    #print vlan_interface
    r,c = getRowCol(interface_data)
    if new_trunk == []:
        pass
    else:
        rr,cc = getRowCol(new_trunk)
    rrr,ccc = getRowCol(vlan_interface)

    interface_vlan = []
    for i in range(0,r):
        for j in range(0,rrr):
            if interface_data[i][0] == vlan_interface[j][0]:
                interface_vlan.append(str(interface_data[i][1]) + "," + vlan_interface[j][1])
        if new_trunk == []:
            pass
        else:
            for k in range(0,rr):
                if interface_data[i][0] == new_trunk[k][0]:
                    interface_vlan.append(str(interface_data[i][1]) + "," + new_trunk[k][1])
    #print interface_vlan
    return interface_vlan


#interface_data = New_reArrange(router.getData(router.command(community,ip,IFMIB_ifDescr)))
#trunk = New_reArrange(router.getData(router.command(community,ip,CISCOVTPMIB_vlanTrunkPortDynamicStatus)))
#vlan_interface = New_reArrange_vlan(router.getData(router.command(community,ip,CISCOSMI_ciscoMgmt)))
















#new_interface_data = [i for i in interface_data if not("Vlan" in i or "Null" in i)]
#print new_interface_data
#for i in range(0,len(trunk)):
#    for j in range(0,len(vlan_interface)):
#        if trunk[i] == "trunking(1)":
#            interface_vlan.append(str(new_interface_data[i]) + "," + "trunk")
#            j = j-1
#            break
#        else:
#            interface_vlan.append(str(new_interface_data[i]) + "," + str(vlan_interface[j]))
#            break
    #coll.update({"index":str(index)},{'$set':{"interface_vlan" + str(i):str(interface_vlan[i])}})
    