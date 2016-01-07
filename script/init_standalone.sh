#!/usr/bin/env bash


# script to start a standalone on localhost
# clean everything up

sudo rm -rf /data
rm *.log



echo "killing mongod and mongos"
killall mongod
killall mongos

sleep 5

mkdir -p /data/sa
mongod  --logpath "1.log" --dbpath /data/sa --port 27017  --smallfiles --fork


echo " system initiate it will take 3 sec"
sleep 3



echo
ps -ef |grep mongo


echo
tail -n 1 1.log


