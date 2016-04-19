import socket
from socket import *
import thread
import os
import pymongo
from pymongo import MongoClient
import datetime
from datetime import datetime
import time
import json
import test_traffic as traffic
import numpy
import router as router

def connectDatabase(collectionsName):
    client = MongoClient()
    database = str(collectionsName)
    db = client['test']
    collection = db[database]
    return collection

def connectCollections(collectionsName,collection):
    #collectionsName = "Sun13Mar2016_163108"
    #Sat12Mar2016_181716_traffic_0
    coll = connectDatabase(collectionsName)
    count = coll.count()
    a = []
    for x in coll.find():
        a.append(x)
    for d in a:
        del d['_id']
    b = json.dumps(a)
    c = json.loads(b)
    return c

def makeFile(filename):
    directory = "test_result"
    filename = filename + ".txt"
    if not os.path.exists(directory):
            os.makedirs(directory)
    thefile = open("test_result/"+str(filename),'a')
    thefile.close()
    return filename

def writeFile(data,filename):
    thefile = open("test_result/"+filename,'a')
    for item in data:
        thefile.write("%s\n" % item)
    thefile.close()

def anaysit(collectionsNameTopo,collectionsNameTraff,indexTraffic):
    #collectionsNameTopo = "Sun13Mar2016_163108"
    #collectionsNameTraff = "Sun13Mar2016_163108_traffic_0"
    collectionTop = connectDatabase(collectionsNameTopo)
    collectionTraff = connectDatabase(collectionsNameTraff)
    dataTopo = connectCollections(collectionsNameTopo,collectionTop)
    dataTraffic = connectCollections(collectionsNameTraff,collectionTraff)
    name = str(collectionsNameTraff)+str(indexTraffic)+"_new"

    index_data = []
    cdp_data = []
    cut_data = []
    all_cdp_data = []
    temp2 = []

    for i in range(0,len(dataTopo)):
        index_data.append(dataTopo[i]['index'])
        #print dataTopo[i]['index']
        for j in dataTopo[i]:
            if "new_cdp" in j:
                cdp_data.append(dataTopo[i][j])
        for k in range(0,len(cdp_data)):
            cut_data.append(cdp_data[k].split(",")[1])
        for l in range(0,len(cut_data)):
            all_cdp_data.append(cut_data[l])
        index_data.append(all_cdp_data)
        temp2.append(index_data)
        index_data = []
        cdp_data = []
        all_cdp_data = []
        cut_data = []

    index = []
    interface = []
    all_interface = []
    temp = []

    for i in range(0,len(dataTraffic)):
        index.append(dataTraffic[i]['index'])
        #print dataTraffic[i]['index']
        for j in dataTraffic[i]:
            if "BW_out" in j:
                #print dataTraffic[i][j]
                if "Vlan" in dataTraffic[i][j] or "Back" in dataTraffic[i][j]:
                    pass
                else:
                    interface = []
                    interface.append(dataTraffic[i][j])
                    all_interface.append(interface)
                    #print all_interface
        index.append(all_interface)
        temp.append(index)
        #temp.append(all_interface)
        index = []
        all_interface = []

    final_data = []
    final_index = []
    final = []
    for i in range(0,len(temp2)):
        for j in range(0,len(temp)):
            if temp2[i][0] == temp[j][0]:
                #print temp2[i][0]
                final_index.append(temp2[i][0])
                #print temp[j][0]
                #print "\n"
                #print temp2[i][1]
                #print temp[j][1]
                for k in range(0,len(temp2[i][1])):
                    for l in range(0,len(temp[j][1])):
                        #print temp2[i][1][k]
                        #print temp[j][1][l][0].split(",")[0]
                        if temp2[i][1][k] == temp[j][1][l][0].split(",")[0]:
                            #print temp2[i][1][k]
                            #print temp[j][1][l][0]
                            #print "kuy"
                            final_data.append(temp[j][1][l][0])
        final_index.append(final_data)
        final.append(final_index)
        final_data = []
        final_index = []

    #print final
    #print final[0]
    #print final[0]
    #print final[0][1]
    coll = connectDatabase(name)
    filename = makeFile(name)

    traffic_cut = []
    test = []
    for i in range(0,len(final)):
        index = final[i][0]
        #print index

        for j in range(0,len(final[i][1])):
            #print final[i][1][j]
            test.append(final[i][1][j])
        print test
            
        #print "-------------------------"
        form = {"index":str(index)}
        coll.insert_one(form)
        print len(test)
        for i in range(0,len(test)):

            traffic_cut.append("index : " + str(index) + "," +str(test[i]))
            coll.update({"index":str(index)},{'$set':{"BW_out"+str(i):str(test[i])}}) 
        test = []
    #print traffic_cut
    writeFile(traffic_cut,filename)
    return traffic_cut,name



#collectionsNameTopo = "Sun13Mar2016_163108"
#collectionsNameTraff = "Sun13Mar2016_163108_traffic_0"
#aaa = anaysit(collectionsNameTopo,collectionsNameTraff)
#print aaa

#coll = connectDatabase(name)
#filename = makeFile(name)

#traffic_cut = []
#for i in range(0,len(data)):
#    index = data[i][0]
#    form = {"index":str(index)}
#    coll.insert_one(form)
#    for j in range(0,len(data[i][1])):
#        print data[i][1][j]
#        traffic_cut.append("index : " + str(index) + "," +str(data[i][1][j]))
#        coll.update({"index":str(index)},{'$set':{"BW_out"+str(j):data[i][1][j]}})
#    print "-------------------------"

#writeFile(traffic_cut,filename)

