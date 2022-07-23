#!/bin/bash
while true
do
    SERVER_IP_ADDRESS='54.244.44.152'
    curl "http://${SERVER_IP_ADDRESS}"
    sleep 1s
    curl "http://${SERVER_IP_ADDRESS}"
    sleep 1s
    curl "http://${SERVER_IP_ADDRESS}/test.html"
    sleep 1s
done