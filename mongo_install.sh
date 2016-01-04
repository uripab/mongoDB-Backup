#!/usr/bin/env bash
echo -----------------------------------------------------------------
echo -                    Mongo - Ubuntu 14.04                       -
echo -----------------------------------------------------------------

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927


#echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
echo 'deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse' | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list


sudo apt-get update


#This is to install the latest stable version
sudo apt-get install -y mongodb-org
