import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import interfacedetail as id
import done_notdontlist as fl
import cdps as cdps

#community = "test"
#your_ip = "192.168.1.1"
#ip = "192.168.1.2"

### OID ###
SNMPv2MIB_sysName = ".1.3.6.1.2.1.1.5"
SNMPv2MIB_sysDescr = ".1.3.6.1.2.1.1.1"
IPMIB_ipAdEntAddr = ".1.3.6.1.2.1.4.20.1.1"
IPMIB_ipAdEntIfIndex = ".1.3.6.1.2.1.4.20.1.2"
IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
IPMIB_ipAdEntNetMask = ".1.3.6.1.2.1.4.20.1.3"

IFMIB_ifInOctets = ".1.3.6.1.2.1.2.2.1.10"
IFMIB_ifOnOctets = ".1.3.6.1.2.1.2.2.1.16"
IFMIB_ifSpeed = ".1.3.6.1.2.1.2.2.1.5"

IPMIB_ipNetToMediaNetAddress = ".1.3.6.1.2.1.4.22.1.3"
CISCOCDPMIB_cdpInterfaceName = ".1.3.6.1.4.1.9.9.23.1.1.1.1.6"
CISCOCDPMIB_cdpCacheDeviceId = ".1.3.6.1.4.1.9.9.23.1.2.1.1.6"
CISCOCDPMIB_cdpCacheDevicePort = ".1.3.6.1.4.1.9.9.23.1.2.1.1.7"
###########
#done_list = []
#notdone_list = []
#newData = []
#newCDP = []
#index = 0

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

def writeFile(data,filename):
    #directory = "result"
    #filename = datetime.now()
    ### path ###
    #if not os.path.exists(directory):
    #    os.makedirs(directory)
    ############
    thefile = open("test_result/"+filename,'a')
    for item in data:
        thefile.write("%s\n" % item)
    thefile.close()

def name():
    databaseName = datetime.now()
    databaseName = databaseName.strftime('%a%d%b%Y_%H%M%S')
    return databaseName

def makeFile(filename):
    directory = "test_result"
    filename = filename + ".txt"
    if not os.path.exists(directory):
            os.makedirs(directory)
    thefile = open("test_result/"+str(filename),'a')
    thefile.close()
    return filename

def connectDatabase(collectionsName):
    client = MongoClient()
    database = str(collectionsName)
    db = client['test']
    collection = db[database]
    return collection

def router(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community):
    ##find interface of target router
    name_data = reArrange(getData(command(community,ip,SNMPv2MIB_sysName)))
    detail_data = detail(getData(command(community,ip,SNMPv2MIB_sysDescr)))
    ip_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntAddr)))
    subnet_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntNetMask)))
    index_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntIfIndex)))
    interface_data = id.New_reArrange(getData(command(community,ip,IFMIB_ifDescr)))
    #ip_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntAddr)))
    #subnet_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntNetMask)))
    #index_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntIfIndex)))
    #interface_data = reArrange(getData(command(community,ip,IFMIB_ifDescr)))
    #traffic_data = reArrange(getData(command(community,ip,IFMIB_ifInOctets)))

    ## new version
    #name_data = reArrange(getData(command(community,ip,SNMPv2MIB_sysName)))
    interface_data_cdps = cdps.New_reArrange_name(getData(command(community,ip,CISCOCDPMIB_cdpInterfaceName)))
    name_cdp_cdps = cdps.New_reArrange_cdpname(getData(command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
    interface_cdps = cdps.New_reArrange_cdpinterface(getData(command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))
    ##
    

    ##find cdp neighbors
    name_cdp = reArrange(getData(command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
    interface_cdp = reArrange(getData(command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))
    ip_cdp = reArrange(getData(command(community,ip,IPMIB_ipNetToMediaNetAddress)))

   
    

    

    #print "name : " + str(name_data)
    #print "detail : " + str(detail_data)
    #print "------------------------------------------------"
    #print "ip : " + str(ip_data)
    #print "subnet : " + str(subnet_data)
    #print "index : " + str(index_data)
    #print "interface_data : " + str(interface_data)
    #print "------------------------------------------------"
    
    #print "name of neighbors : " + str(name_cdp)
    #print "interface of neighbors : " + str(interface_cdp)
    #print "ip of neighbors : " + str(ip_cdp)


    ## add to database : index,router_name,detail
    for i in range(0,len(name_data)):
        form = {"index":str(index),"router_name":str(name_data[i]),"detail":str(detail_data[i])}
        coll.insert_one(form)

    ## type
    type = []
    type.append("router")
    coll.update({"index":str(index)},{'$set':{"type":"router"}})

    ## update interface_detial
  
    newData = []
    newData = id.interfacedetail(ip_data,subnet_data,index_data,interface_data)
    for i in range(0,len(ip_data)):
        done_list.append(ip_data[i])
        coll.update({"index":str(index)},{'$set':{"interface"+str(i):str(newData[i])}}) 


    ## donelist notdonelist
    done_list,notdone_list = fl.findlist(ip_data,ip_cdp,done_list,notdone_list)


    ## update cdp_interface
    newCDP = []    
    for i in range(0,len(name_cdp)):
        newCDP.append(name_cdp[i] + "," + interface_cdp[i])
        coll.update({"index":str(index)},{'$set':{"cdp_interface"+str(i):str(newCDP[i])}}) 

    newCDPs = []
    newCDPs = cdps.New_CDPs(name_data,interface_data_cdps,name_cdp_cdps,interface_cdps)
    for i in range(0,len(newCDPs)):
        coll.update({"index":str(index)},{'$set':{"new_cdp"+str(i):str(newCDPs[i])}}) 

    #print "done : " + str(done_list)
    #print "##############################"
    #print "Not donw : " + str(notdone_list)
    a = name_data + detail_data + type + newData + newCDP + newCDPs
    writeFile(a,filename)
    return done_list,notdone_list,index
