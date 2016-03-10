import paramiko
from netmiko import ConnectHandler
import time

ip = "192.168.1.3"
#port = 22
username = "admin"
password = "admin"
#command = "sh spanning-tree detail | include Port"


def ssh_portstate(host,username,password):
    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(host, username=username, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % host

    # Use invoke_shell to establish an 'interactive session' 
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established"

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("terminal length 0\n")
    remote_conn.send("\n")
    #remote_conn.send("show spanning-tree detail | include VLAN\n")
    remote_conn.send("sh spanning-tree detail | include Port\n")
    # Wait for the command to complete
    time.sleep(2)
    output = remote_conn.recv(5000)
    print output

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
    #for j in range(0,len(data)):
    #    data[j][1] = data[j][1].split("is ")[1];

    for j in range(0,len(data)):
        data[j][1] = data[j][1].split(" of ")[1];

    for j in range(0,len(data)):
        data[j][1] = data[j][1].split(" is ");

    return data

output = ssh_portstate(ip,username,password)
#print output
#print output[0][0]
#print output[0][1][0]
#print output[0][1][1]


#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(ip, username=username, password=password)
