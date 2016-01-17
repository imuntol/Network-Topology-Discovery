import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import test_mongoDB_done as topology

##########
IFMIB_ifInOctets = ".1.3.6.1.2.1.2.2.1.10"
IFMIB_ifOnOctets = ".1.3.6.1.2.1.2.2.1.16"
IFMIB_ifSpeed = ".1.3.6.1.2.1.2.2.1.5"
IFMIB_ifAdminStatus = ".1.3.6.1.2.1.2.2.1.7"
IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
##########

community = "test"
your_ip = "192.168.1.1"
#ip = "192.168.1.2"
ipTraffic = ["192.168.1.2"]
#collectionsName = "aaaaaa"

def traffIn(community,ip):
    In = topology.reArrange(topology.getData(topology.command(community,ip,IFMIB_ifInOctets)))
    return In

def traffOut(community,ip):
    Out = topology.reArrange(topology.getData(topology.command(community,ip,IFMIB_ifOnOctets)))
    return Out

def ifSpeed(community,ip):
    Speed = topology.reArrange(topology.getData(topology.command(community,ip,IFMIB_ifSpeed)))
    return Speed

def checkStatus(community,ip):
    status = topology.reArrange(topology.getData(topology.command(community,ip,IFMIB_ifAdminStatus)))
    return status

def checkInterface(community,ip):
    interface = topology.reArrange(topology.getData(topology.command(community,ip,IFMIB_ifDescr)))
    return interface

def traffic(community,ipTraffic,collectionsName):
    index = 0
    coll = topology.connectDatabase(collectionsName + "_traffic")
    filename = "traffic_" + topology.makeFile(collectionsName)
    newTraffic = []
    for ip in ipTraffic:
        status = checkStatus(community,ip)
        interface = checkInterface(community,ip)

        In_1_data = traffIn(community,ip)
        Out_1_data = traffOut(community,ip)
        start_time = time.time()
        time.sleep(1)
        t = time.time() - start_time
        In_2_data = traffIn(community,ip)
        Out_2_data = traffOut(community,ip)

        ### Speed of each interface
        ifSpeed = ifSpeed(community,ip)

        form = {"index":str(index)}
        coll.insert_one(form)
        temp = 0
        
        for i in range(0,len(In_1_data)-1):
            if status[i] == "up(1)":
                ### *8 for bit and /1024*1024 for Mega
                print "i : " + str(i)
                In = ((int(In_2_data[i]) - int(In_1_data[i]))*8)/(t*1024*1024)
                Out = ((int(Out_2_data[i]) - int(Out_1_data[i]))*8)/(t*1024*1024)
                print "In : " + str(In) + " Mb"
                print "Out : " + str(Out) + " Mb"
                ### find Bandwith Usage in %
                Speed_In = In*100/ifSpeed[i]
                Speed_Out = Out*100/ifSpeed[i]

                newTraffic.append("index : " + str(index) + " = in " + str(In)+" , "+str(interface[i]) + "," +str(Speed_In))
                newTraffic.append("index : " + str(index) + " = out " + str(Out)+" , "+str(interface[i])+ "," +str(Speed_Out))
                coll.update({"index":str(index)},{'$set':{"BW_in"+str(temp):str(In)+","+str(interface[i])+ "," +str(Speed_In)}})
                coll.update({"index":str(index)},{'$set':{"BW_out"+str(temp):str(Out)+","+str(interface[i])+ "," +str(Speed_Out)}})

                temp +=1
        index += 1
    topology.writeFile(newTraffic,filename)

#traffic(community,ipTraffic,"xxxx")
#traffic(community,"192.168.5.2","asdasd")
#traffic(community,"192.168.5.2","asdasd")
#traffic(community,"192.168.5.2","asdasd")
#traffic(community,"192.168.5.2","asdasd")

#status = checkStatus("test","192.168.5.2")