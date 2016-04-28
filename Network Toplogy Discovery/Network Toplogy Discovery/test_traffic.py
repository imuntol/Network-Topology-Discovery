import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import router as router


#community = "test"
#your_ip = "192.168.200.44"
#ip = "192.168.200.3"
#collectionsName = "traffic_test"
##########
IFMIB_ifInOctets = ".1.3.6.1.2.1.2.2.1.10"
IFMIB_ifOnOctets = ".1.3.6.1.2.1.2.2.1.16"
IFMIB_ifSpeed = ".1.3.6.1.2.1.2.2.1.5"
IFMIB_ifOperStatus = ".1.3.6.1.2.1.2.2.1.8"
IFMIB_ifDescr = ".1.3.6.1.2.1.2.2.1.2"
IFMIB_ifMtu = ".1.3.6.1.2.1.2.2.1.4"
##########

def getRowCol(data):
    numrows = len(data)    
    numcols = len(data[0])
    return numrows,numcols

def New_reArrange(data):
    #print data
    for i in range(0,len(data)):
        data[i] = data[i].split(".")[1];
        data[i] = data[i].split("=");
    numrows = len(data)    
    numcols = len(data[0])
    for i in range(0,numrows):
        for j in range(0,numcols):
            if j == 1:
                data[i][j] = data[i][j].split(":")[1].strip()
            else:
                data[i][j] = data[i][j].strip()
    return data

def New_reArrange_Descr(data):
    for i in range(0,len(data)):
        data[i] = data[i].split("r.")[1];
        data[i] = data[i].split("=");
    numrows = len(data)    
    numcols = len(data[0])
    for i in range(0,numrows):
        for j in range(0,numcols):
            if j == 1:
                data[i][j] = data[i][j].split(":")[1].strip()
            else:
                data[i][j] = data[i][j].strip()
    return data

def traffIn(community,ip):
    In = New_reArrange(router.getData(router.command(community,ip,IFMIB_ifInOctets)))
    return In

def traffOut(community,ip):
    Out = New_reArrange(router.getData(router.command(community,ip,IFMIB_ifOnOctets)))
    return Out

def ifSpeed(community,ip):
    #print ip
    #print type(ip)
    Speed = New_reArrange(router.getData(router.command(community,ip,IFMIB_ifSpeed)))
    return Speed

def checkStatus(community,ip):
    status = New_reArrange(router.getData(router.command(community,ip,IFMIB_ifOperStatus)))
    return status

def checkInterface(community,ip):
    interface = New_reArrange_Descr(router.getData(router.command(community,ip,IFMIB_ifDescr)))
    return interface

def packetSize(community,ip):
    size = New_reArrange(router.getData(router.command(community,ip,IFMIB_ifMtu)))
    return size

def ttttt(community,ipTraffic,collectionsName,indexTraffic):
    index = 0
    coll = router.connectDatabase(collectionsName + "_traffic" + "_" + indexTraffic)
    filename = "traffic_" + indexTraffic + "_" + router.makeFile(collectionsName)
    newTraffic = []
    for ip in ipTraffic:
        status = checkStatus(community,ip)
        interface = checkInterface(community,ip)

        start_time = time.time()
        In_1_data = traffIn(community,ip)
        Out_1_data = traffOut(community,ip)
        time.sleep(60)
        In_2_data = traffIn(community,ip)
        Out_2_data = traffOut(community,ip)
        t = time.time() - start_time

        ### Speed of each interface
        ifSpeed = ifSpeed(community,ip)

        form = {"index":str(index)}
        coll.insert_one(form)
        temp = 0
        
        for i in range(0,len(In_1_data)):
            if status[i] == "up(1)" and interface[i] != "Null0":
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
    router.writeFile(newTraffic,filename)

def traffic(community,ipTraffic,collectionsName,indexTraffic):
    index = 0
    
    coll = router.connectDatabase(collectionsName + "_traffic_" + str(indexTraffic))
    filename = "traffic_" + str(indexTraffic) + "_" + router.makeFile(collectionsName)
    newTraffic = []
    for ip in ipTraffic:
        if_Speed = ifSpeed(community,ip)
        check_Status = checkStatus(community,ip)
        check_Interface = checkInterface(community,ip)
        #packet_Size = packetSize(community,ip)
        r,c = getRowCol(check_Interface)
        ## data_time for traffic_config
        date_time = datetime.now()
        date_time = date_time.strftime('%a%d%b%Y_%H%M%S')
        ##
        start_time = time.time()
        trafficIn_1 = traffIn(community,ip)
        trafficOut_1 = traffOut(community,ip)
        #print "traffic in 1 " ,trafficIn_1
        #print "traffic out 1 " ,trafficOut_1
        time.sleep(1)
        trafficIn_2 = traffIn(community,ip)
        trafficOut_2 = traffOut(community,ip)
        #print "traffic in 2 " ,trafficIn_2
        #print "traffic out 2 " ,trafficOut_2
        delta_time = time.time() - start_time
        ## make information
        form = {"index":str(index)}
        coll.insert_one(form)
        ##
        temp = 0
        
        print "index : " + str(index)
        for i in range(0,r):
            if check_Status[i][1] == "up(1)" and check_Interface[i][1] !="Null0":
                
                #print check_Interface[i][1]
                ### *8 for bit and /1024*1024 for Mega
                #print "-----------------------------------in2 - in1 :" , int(trafficIn_2[i][1]) - int(trafficIn_1[i][1])
                #print "-----------------------------------out2 - out1 :" , int(trafficOut_2[i][1]) - int(trafficOut_1[i][1])

                In = round(((float(trafficIn_2[i][1])*8) - (float(trafficIn_1[i][1])*8))/(1024*1024),2)
                Out = round(((float(trafficOut_2[i][1])*8) - (float(trafficOut_1[i][1])*8))/(1024*1024),2)
                #In = ((float(trafficIn_2[i][1]) - float(trafficIn_1[i][1])))/(delta_time)
                #Out = ((float(trafficOut_2[i][1]) - float(trafficOut_1[i][1])))/(delta_time)

                print "---------------------------------------------------"

                print "In b/s : " + str(In*1024*1024)
                print "Out b/s : " + str(Out*1024*1024)
                print "total : " +str((In+Out)*1024*1024)
                print "---------------------------------------------------"
                print "---------------------------------------------------"
                print "In Mb/s : " + str(In)
                print "Out Mb/s : " + str(Out)
                print "total : " +str((In+Out))
                print "---------------------------------------------------"

                #print check_Interface[2][1]

                ## for test
                #In_a = ((float(trafficIn_2[2][1]) - float(trafficIn_1[2][1])))/(delta_time)
                #Out_a = ((float(trafficOut_2[2][1]) - float(trafficOut_1[2][1])))/(delta_time)
                

                ### find Bandwith Usage in %
                #print In,Out
                Speed_In = round(In*100*1024*1024/int(if_Speed[i][1]))
                Speed_Out = round(Out*100*1024*1024/int(if_Speed[i][1]))
                #Speed_In = round(Speed_In,2)
                #Speed_Out = round(Speed_Out,2)
                #print Speed_In,Speed_Out

                #newTraffic.append("index : " + str(index) + " = in " + str(In)+" , "+str(check_Interface[i][1]) + "," +str(Speed_In))
                #newTraffic.append("index : " + str(index) + " = out " + str(Out)+" , "+str(check_Interface[i][1])+ "," +str(Speed_Out))


                newTraffic.append("index : " + str(index) + "," +str(check_Interface[i][1]) +"," + str(In)+","+ str(Speed_In)+"%")
                newTraffic.append("index : " + str(index) + "," +str(check_Interface[i][1]) +"," + str(Out)+","+ str(Speed_Out)+"%")
                coll.update({"index":str(index)},{'$set':{"BW_in"+str(temp):str(check_Interface[i][1]) + "," + str(In) + "," + str(Speed_In)+"%"}})
                coll.update({"index":str(index)},{'$set':{"BW_out"+str(temp):str(check_Interface[i][1]) + "," + str(Out) + "," + str(Speed_Out)+"%"}})

                temp +=1
        index +=1
        print "\n"
        #print check_Interface[2][1]
        #In_a = ((float(trafficIn_2[2][1]) - float(trafficIn_1[2][1])))/(delta_time)
        #Out_a = ((float(trafficOut_2[2][1]) - float(trafficOut_1[2][1])))/(delta_time)
        #avg = avg + In_a + Out_a
        #avg = avg/n
        #print "Avg : " +str(avg)
    indexTraffic = int(indexTraffic) + 1 # +1 = 5 min
    router.writeFile(newTraffic,filename)
    return indexTraffic,date_time


#avg = 0
#x = 0
#avg_all = []
#while (True):

#    ipTraffic = []
#    ipTraffic.append(ip)
#    collectionsName = "testping"
#    indexTraffic = 0
    
#    in_a,out_a =traffic(community,ipTraffic,collectionsName,indexTraffic)
#    print in_a
#    print out_a
#    data = (in_a + out_a)
#    avg_all.append(data)

#    for i in range(0,len(avg_all)):
#        x += avg_all[i]
#    x = x/len(avg_all)
#    print "Avg : " +str(x)
    

#if_Speed = ifSpeed(community,ip)
#print if_Speed

#trafficIn = traffIn(community,ipTraffic)
#print trafficIn
#traffOut = traffOut(community,ipTraffic)
#print traffOut
#ifSpeed = ifSpeed(community,ipTraffic)
#print ifSpeed
#checkStatus = checkStatus(community,ipTraffic)
#print checkStatus
#checkInterface = checkInterface(community,ipTraffic)
#print checkInterface
#packetSize = packetSize(community,ipTraffic)
#print packetSize


#print getRowCol(trafficIn)
#print getRowCol(traffOut)
#print getRowCol(ifSpeed)
#print getRowCol(checkStatus)
#r,c = getRowCol(checkInterface)
#print getRowCol(packetSize)