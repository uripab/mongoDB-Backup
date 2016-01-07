#!/bin/bash

sudo apt-get install -y python-pip
sudo pip install virtualenv

virtualenv env

env/bin/pip install -r requirements.txt

echo "Python environment created at ./env"
