#!/usr/bin/python
 
import telnetlib
import datetime
 
now = datetime.datetime.now()
 
host = "192.168.0.150" # your router ip
username = "admin" # the username
password = "admin"
filename_prefix = "cisco-backup"
 
tn = telnetlib.Telnet(host)
tn.read_until("Username:")
tn.write(username+"\n")
tn.read_until("Password:")
tn.write(password+"\n")
#tn.write("en"+"\n")
#tn.write(password+"\n")
tn.write("terminal length 0"+"\n")
tn.write("sh spanning-tree detail | include Port"+"\n")
#tn.write(" "+"\n")
tn.write("exit"+"\n")
output=tn.read_all()

#print output
temp = []
data = []
temp.append(output)
#print data
temp[0] = temp[0].split("\r\n")
#print data[0]

for i in temp[0]:
    if "(" in i:
        data.append(i)
#print data
for i in range(0,len(data)):
     data[i] = data[i].split("(")[1];
     data[i] = data[i].split(")");
#print data
#print data[0][0]
for j in range(0,len(data)):
    data[j][1] = data[j][1].split("is ")[1];
    data[j][1] = data[j][1].split(" ")[0];
print data
