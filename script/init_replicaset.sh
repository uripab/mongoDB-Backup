#!/usr/bin/env bash


# script to start a replicaset on localhost
# clean everything up

rm -rf /data
rm 1.log
rm 2.log
rm 3.log


echo "killing mongod and mongos"
killall mongod
killall mongos

sleep 5

mkdir -p /data/rs1 /data/rs2 /data/rs3
mongod --replSet uri_db1 --logpath "1.log" --dbpath /data/rs1 --port 27017 --oplogSize 64 --smallfiles --fork
mongod --replSet uri_db1 --logpath "2.log" --dbpath /data/rs2 --port 27018 --oplogSize 64 --smallfiles --fork
mongod --replSet uri_db1 --logpath "3.log" --dbpath /data/rs3 --port 27019 --oplogSize 64 --smallfiles --fork


mongo --port 27017 << 'EOF'
config = { _id: "uri_db1", members:[
          { _id : 0, host : "localhost:27017" ,priority:2},
          { _id : 1, host : "localhost:27018",priority:0 },
          { _id : 2, host : "localhost:27019" ,priority:1}]};
rs.initiate(config)
EOF

echo " system initiate it will take 60 sec"
sleep 60



echo
ps -ef |grep mongo


echo
tail -n 1 1.log
tail -n 1 2.log
tail -n 1 3.log

