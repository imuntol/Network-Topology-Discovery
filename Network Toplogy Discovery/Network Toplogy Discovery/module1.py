import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import router as router
import portstate as ps

community = "test"
your_ip = "192.168.200.44"
ip = "192.168.200.2"

IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
BRIDGEMIB_dot1dStpPort = "1.3.6.1.2.1.17.2.15.1.1" #stp port
BRIDGEMIB_dot1dStpPortState = ".1.3.6.1.2.1.17.2.15.1.3" #stp port state
BRIDGEMIB_dot1dBasePortIfIndex = ".1.3.6.1.2.1.17.1.4.1.2" # port index
CISCOCDPMIB_cdpCacheDevicePort = ".1.3.6.1.4.1.9.9.23.1.2.1.1.7"
CISCOCDPMIB_cdpCacheDeviceId = ".1.3.6.1.4.1.9.9.23.1.2.1.1.6"

#stp_port = ps.reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dStpPort)))
#print stp_port
#stp_portstate = ps.reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dStpPortState)))
#print stp_portstate
#stp_portindex = ps.reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dBasePortIfIndex)))
#print stp_portindex
#ps_interface_data = ps.New_reArrange(router.getData(router.command(community,ip,IFMIB_ifDescr)))
#print ps_interface_data
#interface_cdp = (router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDevicePort)))
#print interface_cdp
#name_cdp = router.reArrange(router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
#print name_cdp
#name_cdp = (router.getData(router.command(community,ip,CISCOCDPMIB_cdpCacheDeviceId)))
#print name_cdp
#state = True
#while(state):
#	print "What are you thinking ?"
#	a = raw_input("Input : ")
#	print "Output : " + str(a)
#	if a == "exit":
#		state = False