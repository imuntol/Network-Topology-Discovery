import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import router as router
import portstate as ps

community = "test"
your_ip = "192.168.200.33"
ip = "192.168.200.1"

IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
BRIDGEMIB_dot1dStpPort = "1.3.6.1.2.1.17.2.15.1.1" #stp port
BRIDGEMIB_dot1dStpPortState = ".1.3.6.1.2.1.17.2.15.1.3" #stp port state
BRIDGEMIB_dot1dBasePortIfIndex = ".1.3.6.1.2.1.17.1.4.1.2" # port index


stp_port = ps.reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dStpPort)))
print stp_port
stp_portstate = ps.reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dStpPortState)))
print stp_portstate
stp_portindex = ps.reArrange(ps.getData(ps.command(community,ip,BRIDGEMIB_dot1dBasePortIfIndex)))
print stp_portindex
#ps_interface_data = ps.New_reArrange(router.getData(router.command(community,ip,IFMIB_ifDescr)))
#print ps_interface_data