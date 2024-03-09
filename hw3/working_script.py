import libvirt
import random
import time
from xml.dom import minidom
import xml.etree.ElementTree as ET
import paramiko
import os
import json

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

if not os.path.isdir('./macs/'):
    os.mkdir(path='./macs/')

mac_list = {}
for host in host_list:
    host_name, host_ip, host_user, host_pass = host.split(',')
    # print(host_name, host_user, host_pass)
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # pkey = paramiko.RSAKey.from_private_key_file('/home/vmadm/.ssh/id_rsa', password='<password_here>') #key1
    # pkey = paramiko.RSAKey.from_private_key_file('/home/vmadm/megh/key')
    client.connect(host_ip, username=host_user, password=host_pass)
    #client.connect(host_ip, pkey=pkey, passphrase=host_pass)
    sftp_client = client.open_sftp()
    res = sftp_client.put(localpath='./mac_gatherer.py', remotepath='/tmp/mac_gatherer.py')
    _stdin, _stdout,_stderr = client.exec_command('sudo python3 /tmp/mac_gatherer.py')
    # print(_stdout.read().decode())
    res = sftp_client.get(localpath='./macs/' + host_name + '.txt', remotepath='/tmp/result.txt')
    print(host_name + ':')
    file = open('./macs/' + host_name + '.txt', mode='r')
    contents = file.read()
    mac_addresses = json.loads(contents)
    for guest_vm in mac_addresses:
        print(guest_vm + ':')
        for net_interface in mac_addresses[guest_vm]:
            print('\t' + net_interface.split('-')[0] + ':\t' + mac_addresses[guest_vm][net_interface])
        print('\n')
    print('\n')

    for vm in mac_addresses:
        for net_interface in mac_addresses[vm]:
            if mac_addresses[vm][net_interface] not in mac_list:
                mac_list[mac_addresses[vm][net_interface]] = net_interface + '-' + host_name
            else:
                print('Duplicate MAC Address found at ' + net_interface + ' in host ' + host_name)