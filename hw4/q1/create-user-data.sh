#!/bin/bash
ssh_key=$1

sudo touch ./user-data
sudo cat << EOF > ./user-data
#cloud-config
disable_root: false
ssh_authorized_keys:
- ssh-rsa
  $ssh_key
users:
- name: root
  lock_passwd: false
  plain_text_passwd: 'root'
- name: ubuntu
  lock_passwd: false
  plain_text_passwd: 'ubuntu'
EOF
exit 0

