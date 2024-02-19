#!/bin/bash
vm_name=$1

sudo touch ./meta-data
sudo cat << EOF > ./meta-data
#cloud-config
instance-id: $vm_name
local-hostname: $vm_name
EOF
#echo '#cloud-config' >> meta-data.yaml
#echo instance-id: $vm_name >> meta-data.yaml
#echo 'local-hostname': $vm_name >> meta-data.yaml
exit 0
