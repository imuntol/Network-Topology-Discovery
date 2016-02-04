import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import router as router
#import test_switch as switch
import check_device as check
import topology as topo

##a = ['Vlan1', 'Vlan100', 'Vlan200', 'FastEthernet0/1', 'FastEthernet0/2', 'FastEthernet0/3', 'FastEthernet0/4', 'FastEthernet0/5', 'FastEthernet0/6', 'FastEthernet0/7', 'FastEthernet0/8', 'FastEthernet0/9', 'FastEthernet0/10', 'FastEthernet0/11', 'FastEthernet0/12', 'FastEthernet0/13', 'FastEthernet0/14', 'FastEthernet0/15', 'FastEthernet0/16', 'FastEthernet0/17', 'FastEthernet0/18', 'FastEthernet0/19', 'FastEthernet0/20', 'FastEthernet0/21', 'FastEthernet0/22', 'FastEthernet0/23', 'FastEthernet0/24', 'GigabitEthernet0/1', 'GigabitEthernet0/2', 'Null0']

community = "test"
your_ip = "192.168.100.50"
ip = "192.168.100.1"

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
CISCOVTPMIB_vtpVlanName = "1.3.6.1.4.1.9.9.46.1.3.1.1.4"
########### forwarding blocking
BRIDGEMIB_dot1dStpPort = "1.3.6.1.2.1.17.2.15.1.1" #stp port
BRIDGEMIB_dot1dStpPortState = ".1.3.6.1.2.1.17.2.15.1.3" #stp port state
#BRIDGEMIB_dot1dBasePort = ".1.3.6.1.2.1.17.1.4.1.1" #
BRIDGEMIB_dot1dBasePortIfIndex = ".1.3.6.1.2.1.17.1.4.1.2" # port index

#IFMIB_ifIndex
#IFMIB_ifDescr

#def switch(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community):
  


#print name_data
#print detail_data
#print ip_data
#print subnet_data
#print index_data
#print interface_data
#print name_cdp
#print interface_cdp
#print ip_cdp
#print vlan_interface
#print "------------------------------------------------"

def switch(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community):

    name_data = router.reArrange(router.getData(router.command(community,ip,SNMPv2MIB_sysName)))
    detail_data = router.detail(router.getData(router.command(router.community,ip,SNMPv2MIB_sysDescr)))
    ip_data = router.reArrange(router.getData(router.command(community,ip,IPMIB_ipAdEntAddr)))
    subnet_data = router.reArrange(router.getData(router.command(community,ip,IPMIB_ipAdEntNetMask)))
    index_data = router.reArrange(router.getData(router.command(community,ip,IPMIB_ipAdEntIfIndex)))
    interface_data = router.reArrange(router.getData(router.command(community,ip,IFMIB_ifDescr)))


    name_cdp = router.reArrange(router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
    interface_cdp = router.reArrange(router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))
    ip_cdp = router.reArrange(router.getData(router.command(community,ip,IPMIB_ipNetToMediaNetAddress)))

    vlan_interface = router.reArrange(router.getData(router.command(community,ip,CISCOSMI_ciscoMgmt)))
    ### forwarding blocking
    stp_port = router.reArrange(router.getData(router.command(community,ip,BRIDGEMIB_dot1dStpPort)))
    stp_portstate = router.reArrange(router.getData(router.command(community,ip,BRIDGEMIB_dot1dStpPortState)))
    stp_portindex = router.reArrange(router.getData(router.command(community,ip,BRIDGEMIB_dot1dBasePortIfIndex)))
    vlan_index = router.reArrange(router.getData(router.command(community,ip,IFMIB_ifIndex)))
    vtp_vlanname = router.reArrange(router.getData(router.command(community,ip,CISCOVTPMIB_vtpVlanName)))
    #vlan_interface
    #interface_data

    #print stp_port
    #print stp_portstate
    #print stp_portindex
    #print vlan_index
    #print vlan_interface
    #print interface_data



    ## add to database : index,switch_name,detail
    for i in range(0,len(name_data)):
            form = {"index":str(index),"switch_name":str(name_data[i]),"detail":str(detail_data[i])}
            coll.insert_one(form)

    ## type
    type = []
    type.append("switch")
    coll.update({"index":str(index)},{'$set':{"type":"switch"}})

    ## vlan , vlan_name
    vlan_name = []
    vlan = [i for i in interface_data if ("Vlan" in i)]
    for i in range(0,len(vlan)):
        vlan_name.append(vlan[i] + "," + vtp_vlanname[i])
        coll.update({"index":str(index)},{'$set':{"vlan_name"+str(i):str(vlan_name[i])}}) 
    
    ## vlan , ip , subnet
    newData = []
    for i in range(0,len(ip_data)):
        done_list.append(ip_data[i])
        newData.append("Vlan" + index_data[i] + "," + ip_data[i] + "," + subnet_data[i])
        coll.update({"index":str(index)},{'$set':{"vlan_ip"+str(i):str(newData[i])}}) 

    ## interface , vlan
    interface_vlan = []
    new_interface_data = [i for i in interface_data if not("Vlan" in i or "Null" in i)]
    for i in range(0,len(new_interface_data)):
        interface_vlan.append(new_interface_data[i] + "," + vlan_interface[i])
        coll.update({"index":str(index)},{'$set':{"interface_vlan" + str(i):str(interface_vlan[i])}})

    ## interface , state
    interface_state = []
    for i in range(0,len(stp_port)):
        if stp_portindex[i] == "No Such Instance currently exists at this OID":
            break
        else:
            for j in range(0,len(vlan_index)):
                if stp_portindex[(int(stp_port[i])-1)] == vlan_index[j]:
                    interface_state.append(str(interface_data[j]) + "," + str(stp_portstate[i]))
                    coll.update({"index":str(index)},{'$set':{"interface_state"+str(i):str(interface_state[i])}})
                    break
                    

    ## check ip that already get data
    for j in range(0,len(done_list)):
        if done_list[j] in ip_cdp:
            ip_cdp.remove(str(done_list[j]))
            j = j-1
    ## make list for ip that didnt get data yet
    for k in range(0,len(ip_cdp)):
        notdone_list.append(ip_cdp[k])

    ## update cdp_interface
    newCDP = []
    for i in range(0,len(name_cdp)):
            newCDP.append(name_cdp[i] + "," + interface_cdp[i])
            coll.update({"index":str(index)},{'$set':{"cdp_interface"+str(i):str(newCDP[i])}}) 

    a = name_data + detail_data + type + vlan_name + newData + interface_vlan + interface_state + newCDP
    router.writeFile(a,filename)
    return done_list,notdone_list,index