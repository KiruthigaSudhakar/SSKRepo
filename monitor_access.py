import paramiko
from scp import SCPClient
import subprocess
import os

def connect_fm_server(ip, user, password, target_port):
    """
    To Connect to Fuel Master Server
    :return: Return the SSH Connection Object
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect(self.fuel_master_ip,
    #               username=self.fuel_master_user,
    #               password=self.fuel_master_password)
    #target_port = 22
    client.connect(hostname = ip,
                   port=target_port,
                   username = user,
                   password = password)
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

    def scp_file_to_remote(self, client, source, destination):
        """
        To transfer files via scp from one machine to remote.
        :return: Returns the status
        """
        scp = SCPClient(client.get_transport())
        scp.put(source, destination)

    def replace_file_content(self, infile, outfile, oldvalue, newvalue):

        """
        To replace the contents of one file to another
        # Change the file content
        # filein = "resources/config_file.txt"
        # fileout = "resources/config_sample.txt"
        :return: Returns the status
        """
        f = open(infile, 'r')
        filedata = f.read()
        f.close()

        newdata = filedata.replace(oldvalue, newvalue)

        f = open(outfile, 'w')
        f.write(newdata)
        f.close()

def get_vm_ip():
    # Get list of running vms
    val = subprocess.Popen(["VBoxManage","list","runningvms"], shell=True, stdout=subprocess.PIPE)
    vm_list = val.communicate()[0]

    vm_id = vm_list.split("\"")[1].split("\"")[0]
    print("The VM id is : \n" + vm_id)

    # Get the ip address of the running vm
    cmd = "VBoxManage guestproperty get " + vm_id + " \"/VirtualBox/GuestInfo/Net/1/V4/IP\" "
    val = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ip_list = val.communicate()[0]
    print("The IP of the Running VM is : " + ip_list.split("Value: ")[1].strip())
    return ip_list.split("Value: ")[1].strip()


def trigger_webserver1():
    v0 = os.system(r"ipconfig")
    print v0
    file = '\"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe\" list runningvms'
    print file
    #v1 = os.system(file)
    #print v1
    #v2 = os.system("dir")
    #print v2
    v = os.popen("VBoxManage list runningvms").readlines()
    #x = v.split("{")[1].split("}")[0]
    print v

#trigger_webserver1()
ip = get_vm_ip()
vm_username = 'vagrant'
vm_password = 'vagrant'
ssh_default_port = 22
#ssh = connect_fm_server('127.0.0.1', 'vagrant', 'vagrant', 2222)
ssh = connect_fm_server(ip.strip(), vm_username, vm_password, ssh_default_port)
# move to home directory
output = send_command_fm_node(ssh, 'cd /home/vagrant')
# Remove any existing index files
output = send_command_fm_node(ssh, 'rm index.html*')
print output
# Iss
cmd = 'wget http://' + ip + ':80'
print cmd
output0 = send_command_fm_node(ssh, cmd)
output1 = send_command_fm_node(ssh, 'ls -l')

print output0
print output1

