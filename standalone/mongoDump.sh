#!/usr/bin/env bash


#Usage:
#    mongorestore <options> <directory or file to restore>


#Restore backups generated with mongodump to a running server.

#Specify a database with -d to restore a single database from the target directory,
#or use -d and -c to restore a single collection from a single .bson file.

echo dump database from host $1 port number $2



echo -----------------------------------------------------------------
echo -                   start dump database
echo -----------------------------------------------------------------

mongodump --host $1:$2


echo -----------------------------------------------------------------
echo -                   end restore database
echo -----------------------------------------------------------------



echo -----------------------------------------------------------------
echo -                   list of back directory in dump    ls -la dump
echo -----------------------------------------------------------------



ls -la dump
