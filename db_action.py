__author__ = 'Uriel Pavlov'

import time
import subprocess
import shlex
import bu_students

STANDALONE_RESTORE_PATH = './standalone/mongoRestore.sh'
STANDALONE_DUMP_PATH = './standalone/mongoDump.sh'
REPLICASET_RESTORE_PATH = './replica-set/mongoRestore.sh'
REPLICASET_DUMP_PATH = './replica-set/mongoDump.sh'
INIT_REPLICA_PATH = './script/init_replicaset.sh'
INIT_SHARD_PATH = './script/init_shard.sh'
LOCALHOST ='localhost'
STANDALONE_PORT_27017 ='27017'
REPLICASET_SEONDARY_PORT_27018 ='27018'
REPLICASET_PRIMARY_PORT_27017 ='27017'
SHARD_1_PRIMARY_PORT_37017 ='37017'
SHARD_2_PRIMARY_PORT_47017 = '47017'
SHARD_3_PRIMARY_PORT_57017 = '57017'
SHARD_1_SEONDARY_PORT_37018 ='37018'
SHARD_2_SEONDARY_PORT_47018 ='47018'
SHARD_3_SEONDARY_PORT_57018 ='57018'
SHARD_CONFIG_SERVER_PORT_57040 ='57040'
STANDALONE ="standalone"
REPLICASET ="replicaset"
SHARDING ="sharding"
STANDALONE_DUMP_FILE_PATH ="dump_standalone"
REPLICASET_DUMP_FILE_PATH ="dump_replicaset"
SHARD_1_DUMP_PATH ="dump_shard_1"
SHARD_2_DUMP_PATH ="dump_shard_2"
SHARD_3_DUMP_PATH ="dump_shard_3"
CONFIG_SERVER_DUMP_PATH ="dump_config_server"

def initiate_standalone():
    print "init standalone"
    # subprocess.call(INIT_REPLICA_PATH)

def initiate_replicaset():
    print "init replicaset"
    print shlex.split('{}'.format(INIT_REPLICA_PATH))
    user_choice = raw_input("initiate replica-set y/n: ")
    if user_choice =='y' or user_choice =='Y':
        print "uri try =",shlex.split('{}'.format(INIT_REPLICA_PATH))
        # subprocess.call(shlex.split('{}'.format(INIT_REPLICA_PATH)))
        subprocess.call([INIT_REPLICA_PATH])

def initiate_sharding():
    print "init sharding"
    print shlex.split('URI {}'.format(INIT_SHARD_PATH))
    user_choice = raw_input("initiate shard y/n: ")
    if user_choice =='y' or user_choice =='Y':
        print "uri try =",shlex.split('{}'.format(INIT_SHARD_PATH))
        subprocess.call(shlex.split('{}'.format(INIT_SHARD_PATH)))

def stop_blancer():
    print "*********************STOP BLANCER*********************\n"
    print "******************************************************"
    time.sleep(5)

def start_blancer():
    print "*********************START BLANCER*********************\n"
    print "******************************************************"
    time.sleep(5)


def mongo_dump_and_restore(path,host,port,dump_path):
    print shlex.split('{} {} {} {}'.format(path,host ,port,dump_path))
    subprocess.call(shlex.split('{} {} {} {}'.format(path,host ,port,dump_path)))

def mongodb_action(deployment):
    while True:
        print " a - add student "
        print " d - delete students "
        print " b - backup db "
        print " r - restore db "
        print " i - insert all student"
        print " q - return to main menu "
        user_choice = raw_input("Enter choice: ")
        if user_choice == 'q':
            break
        elif user_choice == 'a':
            new_student = { }
            new_student['first_name'] = raw_input("Enter first name: ")
            new_student['last_name'] = raw_input("Enter last name: ")
            new_student['course'] = {}
            bu_students.add_student(new_student)
        elif user_choice == 'b':
            if deployment =="standalone":
                mongo_dump_and_restore(STANDALONE_DUMP_PATH, LOCALHOST, STANDALONE_PORT_27017,STANDALONE_DUMP_FILE_PATH)
            elif deployment =="replicaset":
                mongo_dump_and_restore(REPLICASET_DUMP_PATH, LOCALHOST, REPLICASET_SEONDARY_PORT_27018,REPLICASET_DUMP_FILE_PATH)
            elif deployment =="sharding":
                #stop balancer
                stop_blancer()
                #for each shard backup secondary
                print "REPLICASET_DUMP_PATH",REPLICASET_DUMP_PATH
                print "dump shard 1 port {}".format(SHARD_1_SEONDARY_PORT_37018)
                mongo_dump_and_restore(REPLICASET_DUMP_PATH, LOCALHOST, SHARD_1_SEONDARY_PORT_37018,SHARD_1_DUMP_PATH)
                time.sleep(2)
                print "dump shard 2 port {}".format(SHARD_2_SEONDARY_PORT_47018)
                mongo_dump_and_restore(REPLICASET_DUMP_PATH, LOCALHOST, SHARD_2_SEONDARY_PORT_47018,SHARD_2_DUMP_PATH)
                time.sleep(2)
                print "dump shard 3 port {}".format(SHARD_3_SEONDARY_PORT_57018)
                mongo_dump_and_restore(REPLICASET_DUMP_PATH, LOCALHOST, SHARD_3_SEONDARY_PORT_57018,SHARD_3_DUMP_PATH)
                time.sleep(2)
                #backup config server
                print "dump config server  port {}".format(SHARD_CONFIG_SERVER_PORT_57040)
                mongo_dump_and_restore(REPLICASET_DUMP_PATH, LOCALHOST, SHARD_CONFIG_SERVER_PORT_57040,CONFIG_SERVER_DUMP_PATH)
                start_blancer()
            else:
                print "not valid deployment"
                exit(1)
        elif user_choice == 'r':
            if deployment =="standalone":
                mongo_dump_and_restore(STANDALONE_RESTORE_PATH, LOCALHOST, STANDALONE_PORT_27017,STANDALONE_DUMP_FILE_PATH)
            elif deployment =="replicaset":
                print "replica set restore parameters {} {} {} {}".format(REPLICASET_RESTORE_PATH,
                                                                          LOCALHOST,
                                                                          REPLICASET_PRIMARY_PORT_27017,
                                                                          REPLICASET_DUMP_FILE_PATH)
                mongo_dump_and_restore(REPLICASET_RESTORE_PATH,
                                       LOCALHOST,
                                       REPLICASET_PRIMARY_PORT_27017,
                                       REPLICASET_DUMP_FILE_PATH)
            elif deployment =="sharding":
                #for each shard restore primary
                print
                mongo_dump_and_restore(REPLICASET_RESTORE_PATH,
                                       LOCALHOST,
                                       SHARD_1_PRIMARY_PORT_37017,
                                       SHARD_1_DUMP_PATH)
                mongo_dump_and_restore(REPLICASET_RESTORE_PATH,
                                       LOCALHOST,
                                       SHARD_2_PRIMARY_PORT_47017,
                                       SHARD_2_DUMP_PATH)
                mongo_dump_and_restore(REPLICASET_RESTORE_PATH,
                                       LOCALHOST,
                                       SHARD_3_PRIMARY_PORT_57017,
                                       SHARD_3_DUMP_PATH)
                mongo_dump_and_restore(REPLICASET_RESTORE_PATH,
                                       LOCALHOST,
                                       SHARD_CONFIG_SERVER_PORT_57040,
                                       CONFIG_SERVER_DUMP_PATH)
            else:
                print "not valid deployment"
                exit(1)
        elif user_choice == 'd':
            bu_students.delete_student_collection()
        elif user_choice == 'i':
            bu_students.insert_data_to_student_collection()
        else:
            print "I don't know how to {}".format(user_choice)
            time.sleep(1)
            print ""

