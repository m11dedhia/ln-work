#!/bin/bash

iperf3 -c 192.168.38.2 -t 10 -l 64 >> 64.txt
echo "done 1"
iperf3 -c 192.168.38.2 -t 10 -l 128 >> 128.txt
echo "done 2"
iperf3 -c 192.168.38.2 -t 10 -l 256 >> 256.txt
echo "done 3"
iperf3 -c 192.168.38.2 -t 10 -l 512 >> 512.txt
echo "done 4"
iperf3 -c 192.168.38.2 -t 10 -l 1024 >> 1024.txt
echo "done 5"
iperf3 -c 192.168.38.2 -t 10 -l 2048 >> 2048.txt
echo "done 6"
iperf3 -c 192.168.38.2 -t 10 -l 4096 >> 4096.txt
echo "done 7"
iperf3 -c 192.168.38.2 -t 10 -l 8192 >> 8192.txt

exit 1
