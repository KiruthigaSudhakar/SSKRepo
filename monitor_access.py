import paramiko
from scp import SCPClient
import subprocess
import os
import time

def connect_fm_server(ip, user, password, target_port):
    """
    To Connect to Fuel Master Server
    :return: Return the SSH Connection Object
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=ip, port=target_port, username=user, password=password)
    return client


def close_fm_server(self, client):
    """
    To Close Connection to Fuel Master Server
    :return: Returns the status
    """
    return client.close()


def send_command_fm_node(client, command):
    """
    To Close Connection to Fuel Master Server
    :return: Returns the status
    """
    if client:
        stdin, stdout, stderr = client.exec_command(command)
        while not stdout.channel.exit_status_ready():
            # Print data when available
            if stdout.channel.recv_ready():
                alldata = stdout.channel.recv(1024)
                prevdata = b"1"
                while prevdata:
                    prevdata = stdout.channel.recv(1024)
                    alldata += prevdata
                print(str(alldata))
                return str(alldata)
        '''while not stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if stdout.channel.recv_ready():
                rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                if len(rl) > 0:
                    # Print data from stdout
                    logger.info(stdout.channel.recv(1024))'''
    else:
        print("Connection to fuel master not opened.")


def get_vm_ip():
    # Get list of running vms
    val = subprocess.Popen(["VBoxManage", "list", "runningvms"], shell=True, stdout=subprocess.PIPE)
    print val
    vm_list = val.communicate()[0]
    print vm_list
    vm_id = vm_list.split("\"")[1].split("\"")[0]
    print("The VM id is : \n" + vm_id)

    # Get the ip address of the running vm
    cmd1 = "VBoxManage guestproperty get " + vm_id + " \"/VirtualBox/GuestInfo/Net/1/V4/IP\" "
    val = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
    ip_list = val.communicate()[0]
    print("The IP of the Running VM is : " + ip_list.split("Value: ")[1].strip())
    return ip_list.split("Value: ")[1].strip()


def get_vm_ip1():
    # Get list of running vms
    # val = subprocess.Popen(["VBoxManage","list","runningvms"], shell=True, stdout=subprocess.PIPE)
    val = os.popen("VBoxManage list runningvms").readlines()
    print val
    vm_list = val[0]
    vm_id = vm_list.split("\"")[1].split("\"")[0]
    print("The VM id is : \n" + vm_id)

    # Get the ip address of the running vm
    cmd0 = "VBoxManage guestproperty get " + vm_id + " \"/VirtualBox/GuestInfo/Net/1/V4/IP\" "
    val = subprocess.Popen(cmd0, shell=True, stdout=subprocess.PIPE)
    ip_list = val.communicate()[0]
    print("The IP of the Running VM is : " + ip_list.split("Value: ")[1].strip())
    return ip_list.split("Value: ")[1].strip()


def trigger_webserver1():
    v0 = os.system(r"ipconfig")
    print v0
    file = '\"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe\" list runningvms'
    print file
    v = os.popen("VBoxManage list runningvms").readlines()
    print v

pathlist = "C:\Program Files\Oracle\VirtualBox"
vm_username = 'vagrant'
vm_password = 'vagrant'
ssh_default_port = 22
ssh = connect_fm_server('127.0.0.1', 'vagrant', 'vagrant', 2202)
output = send_command_fm_node(ssh, 'cd /home/vagrant')
# Remove any existing index files
output = send_command_fm_node(ssh, 'rm index.html*')
print output
# Is
for i in range(0,10):
    cmd = 'wget http://' + '127.0.0.1' + ':80'
    #print cmd
    output0 = send_command_fm_node(ssh, cmd)
    time.sleep(1)
    cmd = 'wget http://' + '172.28.128.3' + ':80' + '/google.com'
    send_command_fm_node(ssh, cmd)
    time.sleep(2)
    cmd = 'wget http://' + '127.0.0.1' + ':80'
    # print cmd
    output0 = send_command_fm_node(ssh, cmd)
    time.sleep(1)
    cmd = 'wget http://' + '172.28.128.3' + ':80' + '/google.com'
    send_command_fm_node(ssh, cmd)
    time.sleep(2)
    cmd = 'wget http://' + '127.0.0.1' + ':80' + '/php'
    send_command_fm_node(ssh, cmd)
    time.sleep(3)
    cmd = 'wget http://' + '172.28.128.3' + ':80' + '/index.html'
    send_command_fm_node(ssh, cmd)

output2 = send_command_fm_node(ssh, 'ls -l')    
output = send_command_fm_node(ssh, 'rm index.html*')


