import paramiko

ip = "192.168.250.3"
username = "admin"
password = "admin"

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect(ip, username = "admin", password = "admin")
#ssh.send("terminal length 0"+"\n")
#ssh.send("sh spanning-tree detail | include Port"+"\n")
#output = ssh.recv(5000)
#print output