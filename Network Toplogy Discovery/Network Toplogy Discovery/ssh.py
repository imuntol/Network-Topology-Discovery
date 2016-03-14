import paramiko
from netmiko import ConnectHandler
import time

#ip = "192.168.6.7"
###port = 22
#username = "admin"
#password = "admin"
#command = "sh spanning-tree detail | include Port"

def disable_paging(remote_conn):
    '''Disable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

def ssh_portstate(host,username,password):
    check = True

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
    # Strip the initial router prompt
    output = remote_conn.recv(1000)
    # See what we have
    #print output
    # Turn off paging
    disable_paging(remote_conn)

    # Now let's try to send the router a command
    remote_conn.send("\n")
    remote_conn.send("terminal length 0\n")
    remote_conn.send("\n")
    #remote_conn.send("show spanning-tree detail | include VLAN\n")
    while(check):
        remote_conn.send("sh spanning-tree detail | include Port\n")
        # Wait for the command to complete
        time.sleep(2)
        output = remote_conn.recv(5000)
        #print output
        #output = []
        print len(output)
        if len(output) > 0:
            check = False

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
    temp = []
    for i in range(0,len(data)):
        temp.append(str(data[i][0])+","+str(data[i][1][1])+","+str(data[i][1][0]))
    print temp
    remote_conn.close
    #print len(temp)
    return temp

#ip = "192.168.1.1"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.1.2"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.1.3"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.2.4"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.3.5"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.6.6"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.6.7"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.7.8"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.8.9"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#ip = "192.168.8.10"
#output = ssh_portstate(ip,username,password)
#print "--------------------"
#print ip
#print output
#print "--------------------"
#print "\n"

#for i in range(0,len(output)):
#    data.append(str(output[i][0])+","+str(output[i][1][1])+","+str(output[i][1][0]))
#print data
#print len(output)
#print len(output[0])
#print output[0][0]
#print output[0][1][0]
#print output[0][1][1]
#print "--------------------"
#print output[1][0]
#print output[1][1][0]
#print output[1][1][1]


#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect(ip, username=username, password=password)
