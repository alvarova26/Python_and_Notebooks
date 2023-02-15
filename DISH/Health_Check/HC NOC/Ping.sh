#!/bin/bash
date
cat /home/deployment/BE-servers.list |  while read output
do
    ping -c 1 "$output" > /dev/null
    if [ $? -eq 0 ]; then
    echo "node $output is up"
    else
    echo "node $output is down"
    fi
done  > /tmp/DISH_BE_Ping.txt
cat /tmp/DISH_BE_Ping.txt
