copyright:Uriel Pavlov 2016 All rights reserved

Repository for MTA final Msc. project: MongoDB backup process in a distributed system.

The purpose of this program is to demonstrate  and implemant a two stage backup process,
a backup strategy for distributed databases in diffrent deployment systems.


note: This is a work in progress!

pre-requites and setup instructions
install MongodDB version: 3.2.0  by running in root permision:
./install_mongo.sh

install virtualenv run:
sudo python setup.py


system run:
sudo python student_main.py

the system can run in diffrent deployment:
-Standalone
-Replica-Set
-Sharding

gui run:
sudo python gui.py -it will run in localhost:8889

