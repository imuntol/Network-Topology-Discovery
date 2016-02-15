import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import topology as topo
import test_traffic as traffic

community = "test"
your_ip = "192.168.250.44"
ip = "192.168.250.2"

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

indexTraffic = 0

community,ipTraffic,collectionsName = topo.topology(your_ip,ip,community)
#while (True):
#    traffic.traffic(community,ipTraffic,collectionsName,indexTraffic)
#    indexTraffic +=1 # +1 = 5 min
#    time.sleep(5)