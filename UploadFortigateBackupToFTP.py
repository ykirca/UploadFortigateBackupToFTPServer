import sys
import time
import select
import paramiko
import ftplib
import os

host = '192.168.1.1' # Fortigate IP Address
i = 1

while True:
    print 'Trying to connect to %s (%i/30)' % (host, i)
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=22, username='admin', password='admin')
        print "Connected to %s" % host
        break
    except paramiko.AuthenticationException:
        print "Authentication failed when connecting to %s" % host
        sys.exit(1)
    except:
        print "Could not SSH to %s, waiting for it to start" % host
        i += 1
        time.sleep(2)

    # If we could not connect within time limit
    if i == 30:
        print "Could not connect to %s. Giving up" % host
        sys.exit(1)

# Send the command (non-blocking)
stdin, stdout, stderr = ssh.exec_command("show full-configuration")
output = stdout.read()

file = open("forti.txt", "w")
file.write(output)
file.close()

time.sleep(10000)


sftpserver = "192.168.1.2" # FTP server 
port=22

username="root"
password="root"

todayDate = time.strftime("%d-%m-%y")
directory = '/fortigate/' + todayDate
remotefilepath= directory + "/log.txt"

def mk_each_dir(sftp,inRemoteDir):
    currentDir="/"
    for dirElement in inRemoteDir.split("/"):
        if dirElement:
            currentDir += dirElement + "/"
            print ("Try mkdir on :" + currentDir)
            try:
                sftp.mkdir(currentDir)
            except:
                pass


transport = paramiko.Transport((sftpserver, port))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)
print("Connected")


todayDate = time.strftime("%d-%m-%y")
directory = '/hepsipay/'
filename = "log.txt"
mk_each_dir(sftp, directory)
sftp.chdir(directory)
remotefilepath= directory + todayDate + filename
sftp.put("forti.txt", remotefilepath)


sftp.close()
ssh.close()
