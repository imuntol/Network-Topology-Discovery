import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import router as router
import portstate as ps
import interfacevlan as iv
import done_notdontlist as fl
import vlanname as vn
import cdps as cdps
import telnet as t

#community = "test"
#your_ip = "192.168.100.50"
#ip = "192.168.100.1"
#host = "192.168.0.150" # your router ip
#username = "admin" # the username
#password = "admin"


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

CISCOVTPMIB_vlanTrunkPortDynamicStatus = ".1.3.6.1.4.1.9.9.46.1.6.1.1.14" # check trunk port
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

def switch(ip,done_list,notdone_list,filename,index,coll,ipTraffic,community,username,password):
    
    name_data = router.reArrange(router.getData(router.command(community,ip,SNMPv2MIB_sysName)))
    detail_data = router.detail(router.getData(router.command(community,ip,SNMPv2MIB_sysDescr)))
    ip_data = router.reArrange(router.getData(router.command(community,ip,IPMIB_ipAdEntAddr)))
    subnet_data = router.reArrange(router.getData(router.command(community,ip,IPMIB_ipAdEntNetMask)))
    index_data = router.reArrange(router.getData(router.command(community,ip,IPMIB_ipAdEntIfIndex)))
    interface_data = router.reArrange(router.getData(router.command(community,ip,IFMIB_ifDescr)))


    ## new version
    #name_data_cdps = reArrange(getData(command(community,ip,SNMPv2MIB_sysName)))
    interface_data_cdps = cdps.New_reArrange_name(router.getData(router.command(community,ip,CISCOCDPMIB_cdpInterfaceName)))
    name_cdp_cdps = cdps.New_reArrange_cdpname(router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
    interface_cdps = cdps.New_reArrange_cdpinterface(router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))
    ##

    name_cdp = router.reArrange(router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
    interface_cdp = router.reArrange(router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))
    ip_cdp = router.reArrange(router.getData(router.command(community,ip,IPMIB_ipNetToMediaNetAddress)))

    ### forwarding blocking
    stp_port = ps.reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dStpPort)))
    stp_portstate = ps.New_reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dStpPortState)))
    stp_portindex = ps.New_reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dBasePortIfIndex)))
    ps_interface_data = ps.New_reArrange(router.getData(router.command(community,ip,IFMIB_ifDescr)))
    ###
    ### vlan vlan_name
    vtp_vlanname = vn.New_reArrange(router.getData(router.command(community,ip,CISCOVTPMIB_vtpVlanName)))
    ###
    ### interface vlan
    iv_interface_data = iv.New_reArrange(router.getData(router.command(community,ip,IFMIB_ifDescr)))
    trunk = iv.New_reArrange(router.getData(router.command(community,ip,CISCOVTPMIB_vlanTrunkPortDynamicStatus)))
    vlan_interface = iv.New_reArrange_vlan(router.getData(router.command(community,ip,CISCOSMI_ciscoMgmt)))
    ###

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
    #print "------------------------------------------------"
    #print "stp port : " + str(stp_port)
    #print "stp port state : " + str(stp_portstate)
    #print "stp port index : " + str(stp_portindex)
    #print "stp interface : " + str(ps_interface_data)
    #print "------------------------------------------------"
    #print "vlan name : " + str(vtp_vlanname)
    #print "------------------------------------------------"
    #print "interface : " + str(iv_interface_data)
    #print "trunk : " + str(trunk)
    #print "vlan : " + str(vlan_interface)
    #print "------------------------------------------------"

    #print stp_port #"1.3.6.1.2.1.17.2.15.1.1"
    #print stp_portstate #".1.3.6.1.2.1.17.2.15.1.3"
    #print stp_portindex #".1.3.6.1.2.1.17.1.4.1.2"
    #print vlan_index #.1.3.6.1.2.1.2.2.1.1
    #print vlan_interface #"1.3.6.1.4.1.9.9.46.1.3.1.1.4"
    #print interface_data #.1.3.6.1.2.1.2.2.1.2

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
    vlan_name = vn.vlanname(vtp_vlanname)
    for i in range(0,len(vlan_name)):
        coll.update({"index":str(index)},{'$set':{"vlan_name"+str(i):str(vlan_name[i])}}) 
    
    ## vlan , ip , subnet
    newData = []
    for i in range(0,len(ip_data)):
        done_list.append(ip_data[i])
        newData.append("Vlan" + index_data[i] + "," + ip_data[i] + "," + subnet_data[i])
        coll.update({"index":str(index)},{'$set':{"vlan_ip"+str(i):str(newData[i])}}) 

    ## interface , vlan
    interface_vlan = []
    interface_vlan2 = []
    interface_vlan = iv.interfaceVlan(iv_interface_data,trunk,vlan_interface)
    for i in range(0,len(interface_vlan)):
        #print interface_vlan[i]
        interface_vlan2.append(interface_vlan[i])
        coll.update({"index":str(index)},{'$set':{"interface_vlan" + str(i):str(interface_vlan[i])}})
    #interface_vlan2 = []
    #interface_vlan2 = interface_vlan
 
    

    ### interface , state vlan1
    #interface_state = []
    #interface_state = ps.portState(stp_port,stp_portstate,stp_portindex,ps_interface_data)
    #print "state : " + str(interface_state)
    #for i in range(0,len(interface_state)):
    #    coll.update({"index":str(index)},{'$set':{"interface_state" + str(i):str(interface_state[i])}})

    ## interface , state vlan 2 up
    interface_state = []
    interface_state_vlan = []
    interface_state = t.telnet_portstate(ip,username,password)

    interface_state_vlan = t.port_state(interface_vlan,interface_state)
    for i in range(0,len(interface_state_vlan)):
        coll.update({"index":str(index)},{'$set':{"interface_state" + str(i):str(interface_state_vlan[i])}})



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
    a = name_data + detail_data + type + vlan_name + newData + interface_vlan2 + interface_state_vlan + newCDP +newCDPs
    #a = name_data + detail_data + type + vlan_name + newData + interface_vlan  + newCDP
    router.writeFile(a,filename)
    return done_list,notdone_list,index