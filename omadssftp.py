import paramiko
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('192.168.0.220', username='node', password='akZ5obZSIn', port=1220)
except paramiko.SSHException:
    print "Connection Error"
sftp = ssh.open_sftp()
sftp.chdir("/tmp/")
print sftp.listdir()
ssh.close()