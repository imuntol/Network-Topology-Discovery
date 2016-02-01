import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
#import test_traffic as traffic
import router as router
#import test_switch as switch
#import check_device as check
import topology as topo

SNMPv2MIB_sysName = ".1.3.6.1.2.1.1.5"
SNMPv2MIB_sysDescr = ".1.3.6.1.2.1.1.1"
IPMIB_ipAdEntAddr = ".1.3.6.1.2.1.4.20.1.1"
IPMIB_ipAdEntIfIndex = ".1.3.6.1.2.1.4.20.1.2"
IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"

IFMIB_ifInOctets = ".1.3.6.1.2.1.2.2.1.10"
IFMIB_ifOnOctets = ".1.3.6.1.2.1.2.2.1.16"
IFMIB_ifSpeed = ".1.3.6.1.2.1.2.2.1.5"

IPMIB_ipNetToMediaNetAddress = ".1.3.6.1.2.1.4.22.1.3"
CISCOCDPMIB_cdpCacheDeviceId = ".1.3.6.1.4.1.9.9.23.1.2.1.1.6"
CISCOCDPMIB_cdpCacheDevicePort = ".1.3.6.1.4.1.9.9.23.1.2.1.1.7"
#ipTraffic = ['192.168.1.2', '192.168.2.2', '192.168.4.2', '192.168.3.2', '192.168.5.2']
#community = "test"
#databaseName = "abcd"
router_list_end = ['12000','10700','10000','7600','7500','7300','7200','3800','3700','3600','3200','2800','2600','2500','1900','1800','1700','1000','800']
router_list = ['12000','7600','7500','7300','7200','7000','6500','5900','5500','5500','4000','3900','3800','2900','2800','2000','1900','1800','1000','900','800','500']
switch_list_end = ['8110','6200','6100','6000','8600','8500','8400','6500','4000','3750','3750-E','3560-E','3550','2975','2960','2955','2950','2940','2918','2900','2600','2360','2350','1800','1600','1538','1500','500']
switch_list = ['7000','6800','6500','4900','4500','4500-X','3850','3800X','3750','3750-X','3650','3560','3560-C','3560-CX','3560-X','3400X','2960-Plus','2960-S','2960-SF','2960-X','2960-C','2960-CX','2500']
#community,ipTraffic,collectionsName = topology.topology("192.168.1.1","192.168.1.2","test")
#traffic.traffic(community,ipTraffic,collectionsName)

def findCode(community,ip):
    command = router.command(community,ip,SNMPv2MIB_sysDescr)
    data = router.getData(command)
    re_data = router.detail(data)
    re_data = re_data[0].split(",");
    re_data = re_data[1].strip()
    re_data = re_data.split(" ");
    re_data = re_data[0].strip("C");
    return re_data

def checkDevice(code):
    device = "none"
    for i in range(0,len(router_list_end)):
        if code == router_list_end[i]:
            device = "router"
    for i in range(0,len(router_list)):
        if code == router_list[i]:
            device = "router"
    for i in range(0,len(switch_list_end)):
        if code == switch_list_end[i]:
            device = "switch"
    for i in range(0,len(switch_list)):
        if code == switch_list[i]:
            device = "switch"
    return device

#device = checkDevice("12000")
#print device