#!/bin/bash
vm_name=$1
ssh_key=$2
network_name=$3

cd /var/lib/libvirt/images/
#wget 'https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img'
sudo mkdir $vm_name
cd './'$vm_name
sudo qemu-img create -f qcow2 -F qcow2 -o backing_file=/var/lib/libvirt/images/jammy-server-cloudimg-amd64.img ./$vm_name.qcow2
sudo qemu-img resize $vm_name.qcow2 10G
sudo bash /home/vmadm/megh/hw4/q1/create-meta-data.sh $vm_name
sudo bash /home/vmadm/megh/hw4/q1/create-user-data.sh $ssh_key
sudo genisoimage -output ./$vm_name-cidata.iso -volid cidata -joliet -rock ./meta-data ./user-data
sudo virt-install --virt-type kvm --name $vm_name --ram 1024 --vcpus=1 --os-variant ubuntu22.04 --disk path=/var/lib/libvirt/images/$vm_name/$vm_name.qcow2,format=qcow2 --disk path=/var/lib/libvirt/images/$vm_name/$vm_name-cidata.iso,device=cdrom --import --network network=$network_name --noautoconsole
# sudo virsh net-dhcp-leases default
sudo virsh list --all
exit 0

