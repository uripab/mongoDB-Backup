#!/usr/bin/env bash

echo $1

if [ $1 = stop ]
then
    echo stop blancer
    mongo --eval "sh.setBalancerState(false)"
elif [ $1 = start ]
then
    echo start blancer
    mongo --eval "sh.setBalancerState(true)"
else
    echo Unknown parameter
fi
