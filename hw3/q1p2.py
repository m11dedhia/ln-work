import libvirt
import random
import time
from xml.dom import minidom
import xml.etree.ElementTree as ET
import paramiko
import os

num_host = int(input('Number of VMs: '))
# host_file = open('./host_vm_list.txt')
# host_list = host_file.read().split('\n')
host_list = []
for i in range(0, num_host):
    host_ip = input(f'Enter the ip of host {i}: ')
    host_name = input(f'Enter the name of host {i}: ')
    host_user = input(f'Enter the username of host {i}: ')
    host_pass = input(f'Enter the password of host {i}: ')
    host_list.append(host_name + ',' + host_ip + ',' + host_user + ',' + host_pass)

if not os.path.isdir('/home/vmadm/megh/hw3/macs/'):
    os.mkdir(path='/home/vmadm/megh/hw3/macs/')

for host in host_list:
    _, host_name, host_user, host_pass = host.split(',')
    print(host_name, host_user, host_pass)
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # pkey = paramiko.RSAKey.from_private_key_file('/home/vmadm/.ssh/id_rsa', password='<password_here>') #key1
    pkey = paramiko.RSAKey.from_private_key_file('/home/vmadm/megh/key')
    # client.connect(host_name, username=host_user, password=host_pass)
    client.connect(host_name, pkey=pkey, passphrase=host_pass)
    sftp_client = client.open_sftp()
    res = sftp_client.put(localpath='/home/vmadm/megh/hw3/mac_gatherer.py', remotepath='/tmp/mac_gatherer.py')
    _stdin, _stdout,_stderr = client.exec_command('sudo python3 /tmp/mac_gatherer.py')
    print(_stdout.read().decode())
    res = sftp_client.get(localpath='/home/vmadm/megh/hw3/macs/' + host_name + '.txt', remotepath='/home/result.txt')
