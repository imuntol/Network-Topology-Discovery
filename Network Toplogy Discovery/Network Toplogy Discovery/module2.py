#import os
#import pymongo
#from pymongo import MongoClient
#import datetime
#from datetime import datetime
#import time
#import router as router
#import portstate as ps
#import interfacevlan as iv
#import done_notdontlist as fl
#import vlanname as vn
#import cdps as cdps
#import telnet as t

#ip = "192.168.0.150"
#community = "test"
#username = "admin"
#password = "admin"
#### OID ###
#SNMPv2MIB_sysName = ".1.3.6.1.2.1.1.5"
#SNMPv2MIB_sysDescr = ".1.3.6.1.2.1.1.1"
#IPMIB_ipAdEntAddr = ".1.3.6.1.2.1.4.20.1.1"
#IPMIB_ipAdEntIfIndex = ".1.3.6.1.2.1.4.20.1.2"
#IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
#IPMIB_ipAdEntNetMask = ".1.3.6.1.2.1.4.20.1.3"

#IFMIB_ifInOctets = ".1.3.6.1.2.1.2.2.1.10"
#IFMIB_ifOnOctets = ".1.3.6.1.2.1.2.2.1.16"
#IFMIB_ifSpeed = ".1.3.6.1.2.1.2.2.1.5"

#IPMIB_ipNetToMediaNetAddress = ".1.3.6.1.2.1.4.22.1.3"
#CISCOCDPMIB_cdpInterfaceName = ".1.3.6.1.4.1.9.9.23.1.1.1.1.6"
#CISCOCDPMIB_cdpCacheDeviceId = ".1.3.6.1.4.1.9.9.23.1.2.1.1.6"
#CISCOCDPMIB_cdpCacheDevicePort = ".1.3.6.1.4.1.9.9.23.1.2.1.1.7"
############
#IFMIB_ifIndex = ".1.3.6.1.2.1.2.2.1.1" # index
#CISCOSMI_ciscoMgmt = ".1.3.6.1.4.1.9.9.68.1.2.2.1.2" # vlan interface
#CISCOVTPMIB_vtpVlanName = "1.3.6.1.4.1.9.9.46.1.3.1.1.4"
############ forwarding blocking
#BRIDGEMIB_dot1dStpPort = "1.3.6.1.2.1.17.2.15.1.1" #stp port
#BRIDGEMIB_dot1dStpPortState = ".1.3.6.1.2.1.17.2.15.1.3" #stp port state
##BRIDGEMIB_dot1dBasePort = ".1.3.6.1.2.1.17.1.4.1.1" #
#BRIDGEMIB_dot1dBasePortIfIndex = ".1.3.6.1.2.1.17.1.4.1.2" # port index
##IFMIB_ifIndex
##IFMIB_ifDescr

#CISCOVTPMIB_vlanTrunkPortDynamicStatus = ".1.3.6.1.4.1.9.9.46.1.6.1.1.14" # check trunk port
##def switch(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community):
  
#iv_interface_data = iv.New_reArrange(router.getData(router.command(community,ip,IFMIB_ifDescr)))
#trunk = iv.New_reArrange(router.getData(router.command(community,ip,CISCOVTPMIB_vlanTrunkPortDynamicStatus)))
#vlan_interface = iv.New_reArrange_vlan(router.getData(router.command(community,ip,CISCOSMI_ciscoMgmt)))

#interface_vlan = []
#interface_vlan = iv.interfaceVlan(iv_interface_data,trunk,vlan_interface)
#print interface_vlan

#port_state = t.telnet_portstate(ip,username,password)
##print port_state

#for i in range(0,len(interface_vlan)):
#    interface_vlan[i] = interface_vlan[i].split(",");
##print interface_vlan

#data = []
#for i in range(0,len(port_state)):
#    for j in range(0,len(interface_vlan)):
#        if port_state[i][0] == interface_vlan[j][0]:
#            data.append(str(port_state[i][0] + "," + port_state[i][1] + "," + interface_vlan[j][1]))
#print data