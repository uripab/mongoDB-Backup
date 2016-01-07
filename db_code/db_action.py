__author__ = 'Uriel Pavlov'

import time
import subprocess
import shlex
import student_main
from random import randint
from log_manager import db_log

class database_action(object):
    def __init__(self):
        self.STANDALONE_RESTORE_PATH = '../standalone/mongoRestore.sh'
        self.STANDALONE_DUMP_PATH = '../standalone/mongoDump.sh'
        self.REPLICASET_RESTORE_PATH = '../replica-set/mongoRestore.sh'
        self.REPLICASET_DUMP_PATH = '../replica-set/mongoDump.sh'
        self.INIT_STANDALONE_PATH = '../script/init_standalone.sh'
        self.INIT_REPLICA_PATH = '../script/init_replicaset.sh'
        self.INIT_SHARD_PATH = '../script/init_shard.sh'
        self.STOP_AND_START_BLANCER_PATH = '../script/stop_and_start_balancer.sh'
        self.LOCALHOST ='localhost'
        self.STANDALONE_PORT_27017 ='27017'
        self.REPLICASET_SEONDARY_PORT_27018 ='27018'
        self.REPLICASET_PRIMARY_PORT_27017 ='27017'
        self.SHARD_1_PRIMARY_PORT_37017 ='37017'
        self.SHARD_2_PRIMARY_PORT_47017 = '47017'
        self.SHARD_3_PRIMARY_PORT_57017 = '57017'
        self.SHARD_1_SEONDARY_PORT_37018 ='37018'
        self.SHARD_2_SEONDARY_PORT_47018 ='47018'
        self.SHARD_3_SEONDARY_PORT_57018 ='57018'
        self.SHARD_CONFIG_SERVER_PORT_57040 ='57040'
        self.STANDALONE ="standalone"
        self.REPLICASET ="replicaset"
        self.SHARDING ="sharding"
        self.STANDALONE_DUMP_FILE_PATH ="dump_standalone"
        self.REPLICASET_DUMP_FILE_PATH ="dump_replicaset"
        self.SHARD_1_DUMP_PATH ="dump_shard_1"
        self.SHARD_2_DUMP_PATH ="dump_shard_2"
        self.SHARD_3_DUMP_PATH ="dump_shard_3"
        self.CONFIG_SERVER_DUMP_PATH ="dump_config_server"

    def initiate_standalone(self):
        db_log.debug("init standalone")
        print shlex.split('{}'.format(self.INIT_STANDALONE_PATH))
        user_choice = raw_input("initiate standalonet y/n: ")
        if user_choice =='y' or user_choice =='Y':
            subprocess.call(shlex.split('{}'.format(self.INIT_STANDALONE_PATH)))
        # subprocess.call(INIT_REPLICA_PATH)

    def initiate_replicaset(self):
        db_log.debug( "init replicaset")
        print shlex.split('{}'.format(self.INIT_REPLICA_PATH))
        user_choice = raw_input("initiate replica-set y/n: ")
        if user_choice =='y' or user_choice =='Y':
            subprocess.call(shlex.split('{}'.format(self.INIT_REPLICA_PATH)))
            #subprocess.call([self.INIT_REPLICA_PATH])

    def initiate_sharding(self):
        db_log.debug("init sharding")
        print shlex.split(' {}'.format(self.INIT_SHARD_PATH))
        user_choice = raw_input("initiate shard y/n: ")
        if user_choice =='y' or user_choice =='Y':
            subprocess.call(shlex.split('{}'.format(self.INIT_SHARD_PATH)))

    def stop_blancer(self):
        db_log.debug("stop balancer")
        print "*********************STOP BLANCER*********************\n"
        print "******************************************************"
        command ="stop"
        db_log.debug('{} {} '.format(self.STOP_AND_START_BLANCER_PATH,command))
        print shlex.split('{} {}'.format(self.STOP_AND_START_BLANCER_PATH,command))
        subprocess.call(shlex.split('{} {}'.format(self.STOP_AND_START_BLANCER_PATH,command)))
        time.sleep(5)

    def start_blancer(self):
        db_log.debug("start balancer")
        print "*********************START BLANCER*********************\n"
        print "******************************************************"
        command ="start"
        db_log.debug('{} {}'.format(self.STOP_AND_START_BLANCER_PATH,command))
        print shlex.split('{} {}'.format(self.STOP_AND_START_BLANCER_PATH,command))
        subprocess.call(shlex.split('{} {}'.format(self.STOP_AND_START_BLANCER_PATH,command)))
        time.sleep(5)


    def mongo_dump_and_restore(self,path,host,port,dump_path):
        db_log.debug('{} {} {} {}'.format(path,host ,port,dump_path))
        print shlex.split('{} {} {} {}'.format(path,host ,port,dump_path))
        subprocess.call(shlex.split('{} {} {} {}'.format(path,host ,port,dump_path)))

    def mongodb_action(self,deployment):
        '''
        :param deployment: standalone replicaset or sharding
        :return:OK -1
        '''
        my_student =student_main.student()
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
                new_student['student_id']= randint(10000,99999)
                new_student['first_name'] = raw_input("Enter first name: ")
                new_student['last_name'] = raw_input("Enter last name: ")
                new_student['course'] = {}
                my_student.add_student(new_student)
            elif user_choice == 'b':
                if deployment =="standalone":
                    db_log.debug("lock Database")
                    print shlex.split('{} {} {}'.format("mongo", "--eval", "db.fsyncLock()" ))
                    subprocess.call(shlex.split('{} {} {}'.format("mongo", "--eval", "db.fsyncLock()")))
                    time.sleep(5)
                    print "*********************lock Database*********************\n"
                    print "******************************************************"
                    time.sleep(5)
                    self.mongo_dump_and_restore(self.STANDALONE_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.STANDALONE_PORT_27017,
                                                self.STANDALONE_DUMP_FILE_PATH)
                    db_log.debug("Unlock Database")
                    print "*********************Unlock Database*********************\n"
                    print "******************************************************"
                    print shlex.split('{} {} {}'.format("mongo", "--eval", "db.fsyncUnlock()" ))
                    subprocess.call(shlex.split('{} {} {}'.format("mongo", "--eval", "db.fsyncUnlock()")))
                    time.sleep(5)
                elif deployment =="replicaset":
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.REPLICASET_SEONDARY_PORT_27018,
                                                self.REPLICASET_DUMP_FILE_PATH)
                elif deployment =="sharding":
                    #stop balancer
                    self.stop_blancer()
                    #for each shard backup secondary
                    print "REPLICASET_DUMP_PATH",self.REPLICASET_DUMP_PATH
                    print "dump shard 1 port {}".format(self.SHARD_1_SEONDARY_PORT_37018)
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.SHARD_1_SEONDARY_PORT_37018,
                                                self.SHARD_1_DUMP_PATH)
                    time.sleep(2)
                    print "dump shard 2 port {}".format(self.SHARD_2_SEONDARY_PORT_47018)
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.SHARD_2_SEONDARY_PORT_47018,
                                                self.SHARD_2_DUMP_PATH)
                    time.sleep(2)
                    print "dump shard 3 port {}".format(self.SHARD_3_SEONDARY_PORT_57018)
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.SHARD_3_SEONDARY_PORT_57018,
                                                self.SHARD_3_DUMP_PATH)
                    time.sleep(2)
                    #backup config server
                    print "dump config server  port {}".format(self.SHARD_CONFIG_SERVER_PORT_57040)
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.SHARD_CONFIG_SERVER_PORT_57040,
                                                self.CONFIG_SERVER_DUMP_PATH)
                    self.start_blancer()
                else:
                    print "not valid deployment"
                    exit(1)
            elif user_choice == 'r':
                if deployment =="standalone":
                   self.mongo_dump_and_restore(self.STANDALONE_RESTORE_PATH,
                                               self.LOCALHOST,
                                               self.STANDALONE_PORT_27017,
                                               self.STANDALONE_DUMP_FILE_PATH)
                elif deployment =="replicaset":
                    print "replica set restore parameters {} {} {} {}".format(self.REPLICASET_RESTORE_PATH,
                                                                              self.LOCALHOST,
                                                                              self.REPLICASET_PRIMARY_PORT_27017,
                                                                              self.REPLICASET_DUMP_FILE_PATH)
                    self.mongo_dump_and_restore(self.REPLICASET_RESTORE_PATH,
                                           self.LOCALHOST,
                                           self.REPLICASET_PRIMARY_PORT_27017,
                                           self.REPLICASET_DUMP_FILE_PATH)
                elif deployment =="sharding":
                    #for each shard restore primary
                    print
                    self.mongo_dump_and_restore(self.REPLICASET_RESTORE_PATH,
                                           self.LOCALHOST,
                                           self.SHARD_1_PRIMARY_PORT_37017,
                                           self.SHARD_1_DUMP_PATH)
                    self.mongo_dump_and_restore(self.REPLICASET_RESTORE_PATH,
                                           self.LOCALHOST,
                                           self.SHARD_2_PRIMARY_PORT_47017,
                                           self.SHARD_2_DUMP_PATH)
                    self.mongo_dump_and_restore(self.REPLICASET_RESTORE_PATH,
                                           self.LOCALHOST,
                                           self.SHARD_3_PRIMARY_PORT_57017,
                                           self.SHARD_3_DUMP_PATH)
                    self.mongo_dump_and_restore(self.REPLICASET_RESTORE_PATH,
                                           self.LOCALHOST,
                                           self.SHARD_CONFIG_SERVER_PORT_57040,
                                           self.CONFIG_SERVER_DUMP_PATH)
                else:
                    print "not valid deployment"
                    exit(1)
            elif user_choice == 'd':
                my_student.delete_student_collection()
            elif user_choice == 'i':
                my_student.insert_data_to_student_collection()
            else:
                print "I don't know how to {}".format(user_choice)
                time.sleep(1)
                print ""
        return 1

