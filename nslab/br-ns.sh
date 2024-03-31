#!/bin/bash

sudo ip netns add NS1
sudo ip link add bridgeinf1 type veth peer name ns1inf1
sudo ip link set ns1inf1 netns NS1
sudo ip netns exec NS1 ip link set ns1inf1 up
sudo ip link set bridgeinf1 up
sudo ip link set bridgeinf1 master sw1