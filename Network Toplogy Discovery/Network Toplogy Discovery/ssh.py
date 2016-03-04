import paramiko
from netmiko import ConnectHandler

ip = "192.168.1.2"
username = "admin"
password = "admin"

#cisco_881 = {
#'device_type': 'cisco_ios',
#'ip': ip,
#'username': username,
#'password': password,
#} 

net_connect = ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password)
output = net_connect.send_command("sh ip int br")
print output

#temp = []
#data = []
#temp.append(output)
##print data
#temp[0] = temp[0].split("\r\n")
##print data[0]

#for i in temp[0]:
#    if "(" in i:
#        data.append(i)
##print data
#for i in range(0,len(data)):
#     data[i] = data[i].split("(")[1];
#     data[i] = data[i].split(")");
##print data
##print data[0][0]
#for j in range(0,len(data)):
#    data[j][1] = data[j][1].split("is ")[1];
#    data[j][1] = data[j][1].split(" ")[0];
#print data


##ssh = paramiko.SSHClient()
##ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
###ssh.connect(ip, username=username, password=password)
