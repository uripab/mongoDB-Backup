#!/usr/bin/env bash


#Usage:
#    mongorestore <options> <directory or file to restore>


#Restore backups generated with mongodump to a running server.

#Specify a database with -d to restore a single database from the target directory,
#or use -d and -c to restore a single collection from a single .bson file.

echo reatore database from host $1 port number $2



echo -----------------------------------------------------------------
echo -                   start restore database
echo -----------------------------------------------------------------

mongorestore --host $1:$2 --drop dump


echo -----------------------------------------------------------------
echo -                   end restore database
echo -----------------------------------------------------------------



