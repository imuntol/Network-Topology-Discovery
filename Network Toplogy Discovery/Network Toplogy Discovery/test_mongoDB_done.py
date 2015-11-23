import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time

#backup plsssssss version cont
email = "y1moretime@gmail.com"
my_command = "whoami"
ping = "ping 8.8.8.8"
community = "test"
your_ip = "192.168.1.1"
ip = "192.168.1.2"
### OID ###
SNMPv2MIB_sysName = ".1.3.6.1.2.1.1.5"
SNMPv2MIB_sysDescr = ".1.3.6.1.2.1.1.1"
IPMIB_ipAdEntAddr = ".1.3.6.1.2.1.4.20.1.1"
IPMIB_ipAdEntIfIndex = ".1.3.6.1.2.1.4.20.1.2"
IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
IFMIB_ifInOctets = ".1.3.6.1.2.1.2.2.1.10"

IPMIB_ipNetToMediaNetAddress = ".1.3.6.1.2.1.4.22.1.3"

CISCOCDPMIB_cdpCacheDeviceId = ".1.3.6.1.4.1.9.9.23.1.2.1.1.6"
CISCOCDPMIB_cdpCacheDevicePort = ".1.3.6.1.4.1.9.9.23.1.2.1.1.7"
###########
done_list = []
notdone_list = []
newData = []
newCDP = []
index = 0
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
    data[0] = data[0].split("G:")[1];
    data[0] = data[0].strip()
    temp = ""
    for i in range(0,len(data)):
        temp = temp + data[i]
    data = []
    data.append(temp)
    print data
    return data

def reArrange(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("=")[1];
        data[i] = data[i].split(":")[1];
        data[i] = data[i].split(" ")[1];
    print data
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

def makeFile():
    directory = "test_result"
    filename = datetime.now()
    filename = filename.strftime('%d%m%Y_%H%M%S')+".txt"
    if not os.path.exists(directory):
            os.makedirs(directory)
    thefile = open("result/"+str(filename),'a')
    thefile.close()
    return filename

def connectDatabase():
    client = MongoClient()
    databaseName = datetime.now()
    databaseName = databaseName.strftime('%a%d%b%Y_%H%M%S') 
    database = str(databaseName)
    db = client['test']
    collection = db[database]
    return collection

def router(ip,done_list,notdone_list,filename,index):
    ##find interface of target router
    name_data = reArrange(getData(command(community,ip,SNMPv2MIB_sysName)))
    detail_data = detail(getData(command(community,ip,SNMPv2MIB_sysDescr)))
    ip_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntAddr)))
    index_data = reArrange(getData(command(community,ip,IPMIB_ipAdEntIfIndex)))
    interface_data = reArrange(getData(command(community,ip,IFMIB_ifDescr)))
    traffic_data = reArrange(getData(command(community,ip,IFMIB_ifInOctets)))

    ##find cdp neighbors
    name_cdp = reArrange(getData(command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
    interface_cdp = reArrange(getData(command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))
    ip_cdp = reArrange(getData(command(community,ip,IPMIB_ipNetToMediaNetAddress)))

    ## add to database : index,router_name,detail
    for i in range(0,len(name_data)):
        form = {"index":str(index),"router_name":str(name_data[i]),"detail":str(detail_data[i])}
        coll.insert_one(form)

    ## update interface_detial
    newData = []
    for i in range(0,len(ip_data)):
        done_list.append(ip_data[i])
        newData.append(ip_data[i] + "," + interface_data[int(index_data[i])-1] + "," + traffic_data[int(index_data[i])-1])
        coll.update({"index":str(index)},{'$set':{"interface"+str(i):str(newData[i])}}) 

    ## check ip that already get data
    for j in range(0,len(done_list)):
        if done_list[j] in ip_cdp:
            ip_cdp.remove(str(done_list[j]))
            j = j-1

    ## make list for ip that didnt get data yet
    for k in range(0,len(ip_cdp)):
        notdone_list.append(ip_cdp[k])
    #print notdone_list

    ## update cdp_interface
    newCDP = []    
    for i in range(0,len(ip_cdp)):
        newCDP.append(name_cdp[i] + "," + interface_cdp[i])
        coll.update({"index":str(index)},{'$set':{"cdp_interface"+str(i):str(newCDP[i])}}) 
    a = name_data + detail_data + newData + newCDP
    writeFile(a,filename)
    return done_list,notdone_list,index

coll = connectDatabase()
start_time = time.time()
filename = makeFile()
done_list.append(your_ip)
done_list,notdone_list,index = router(ip,done_list,notdone_list,filename,index)
while(notdone_list):
    index += 1
    ip = notdone_list.pop()
    #print ip
    done_list,notdone_list,index = router(ip,done_list,notdone_list,filename,index)
print("--- %s seconds ---" % (time.time() - start_time))