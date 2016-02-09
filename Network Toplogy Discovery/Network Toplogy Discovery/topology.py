import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import router as router
import test_switch as switch
import check_device as check

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
CISCOCDPMIB_cdpCacheDeviceId = ".1.3.6.1.4.1.9.9.23.1.2.1.1.6"
CISCOCDPMIB_cdpCacheDevicePort = ".1.3.6.1.4.1.9.9.23.1.2.1.1.7"
###########
IFMIB_ifIndex = ".1.3.6.1.2.1.2.2.1.1" # index
CISCOSMI_ciscoMgmt = ".1.3.6.1.4.1.9.9.68.1.2.2.1.2" # vlan interface
########### forwarding blocking
BRIDGEMIB_dot1dStpPort = "1.3.6.1.2.1.17.2.15.1.1" #stp port
BRIDGEMIB_dot1dStpPortState = ".1.3.6.1.2.1.17.2.15.1.3" #stp port state
#BRIDGEMIB_dot1dBasePort = ".1.3.6.1.2.1.17.1.4.1.1" #
BRIDGEMIB_dot1dBasePortIfIndex = ".1.3.6.1.2.1.17.1.4.1.2" # port index
#IFMIB_ifIndex
#IFMIB_ifDescr

def topology(your_ip,ip,community):
    print "your ip : " + str(your_ip) +" ip device : " + str(ip) + " community : " + str(community)
    done_list = []
    notdone_list = []
    newData = []
    ipTraffic = []
    index = 0

    start_time = time.time()
    collectionsName = router.name()
    coll = router.connectDatabase(collectionsName)
    filename = router.makeFile(collectionsName)
    done_list.append(your_ip)
    ipTraffic.append(ip)

    print "done list : " + str(done_list)
    print "not done list : " + str(notdone_list)

    code = check.findCode(community,ip)
    device = check.checkDevice(code)
    print "type : " + str(device)
    if device == "router":
        done_list,notdone_list,index = router.router(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community)
    elif device == "switch":
        done_list,notdone_list,index = switch.switch(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community)
    else:
        print "dont know the type of device"
    
    while(notdone_list):
        index += 1
        ip = notdone_list.pop()
       
        print "ip " + str(ip)
        print "done list : " + str(done_list)
        print "not done list : " + str(notdone_list)

        ipTraffic.append(ip)
        code = check.findCode(community,ip)
        if code == []:
            print "skip this ip"
        else:
            device = check.checkDevice(code)
            if device == "router":
                done_list,notdone_list,index = router.router(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community)
            elif device == "switch":
                done_list,notdone_list,index = switch.switch(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community)
            else:
                print "dont know the type of device"
    print("--- %s seconds ---" % (time.time() - start_time))
    return community,ipTraffic,collectionsName