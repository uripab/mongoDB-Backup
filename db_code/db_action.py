__author__ = 'Uriel Pavlov'

import os
import time
import subprocess
import shlex
import student_main
from random import randint
from log_manager import db_log

class database_action(object):
    '''
    class for execute all functionality on database
    '''
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
        '''
        initiate standalone server it delete all previous data
        '''
        db_log.debug("init standalone")
        os.system("clear")
        user_choice = raw_input("initiate standalone  y/n: ")
        if user_choice =='y' or user_choice =='Y':
            subprocess.call(shlex.split('{}'.format(self.INIT_STANDALONE_PATH)))

    def initiate_replicaset(self):
        '''
        initiate replicaset servers- it delete all previous data
        on port 27017 -Primary 27018 27019 secondary
        '''
        db_log.debug( "init replicaset")
        os.system("clear")
        user_choice = raw_input("initiate replica-set y/n: ")
        if user_choice =='y' or user_choice =='Y':
            subprocess.call(shlex.split('{}'.format(self.INIT_REPLICA_PATH)))

    def initiate_sharding(self):
        '''
        initiate shard cluster  servers- it delete all previous data
        in the shard contain 3 shard each shard is replica set
        shard 1   on port 37017 -Primary 37018 37019 secondary
        shard 2   on port 47017 -Primary 47018 47019 secondary
        shard 3   on port 57017 -Primary 57018 57019 secondary
        '''
        db_log.debug("init sharding")
        os.system("clear")
        user_choice = raw_input("initiate shard y/n: ")
        if user_choice =='y' or user_choice =='Y':
            subprocess.call(shlex.split('{}'.format(self.INIT_SHARD_PATH)))

    def stop_blancer(self):
        '''
        this function stop balancer process in shard enviroment
        '''
        db_log.debug("stop balancer")
        print "*********************STOP BLANCER*********************\n"
        print "******************************************************"
        command ="stop"
        db_log.debug('{} {} '.format(self.STOP_AND_START_BLANCER_PATH,command))
        subprocess.call(shlex.split('{} {}'.format(self.STOP_AND_START_BLANCER_PATH,command)))
        time.sleep(5)

    def start_blancer(self):
        '''
        this function stop balancer process in shard enviroment
        '''
        db_log.debug("start balancer")
        print "*********************START BLANCER*********************\n"
        print "******************************************************"
        command ="start"
        db_log.debug('{} {}'.format(self.STOP_AND_START_BLANCER_PATH,command))
        subprocess.call(shlex.split('{} {}'.format(self.STOP_AND_START_BLANCER_PATH,command)))
        time.sleep(5)

    def mongo_dump_and_restore(self,path,host,port,dump_path):
        '''
        function that handle all dump and restore of all deployment
        Standalone Relica-Set and Sharding
        :param path: path to bash scrip
        :param host: ip of db server by default localhost
        :param port: db port
        :param dump_path: path to dump file
        '''
        db_log.debug('{} {} {} {}'.format(path,host ,port,dump_path))
        subprocess.call(shlex.split('{} {} {} {}'.format(path,host ,port,dump_path)))

    def mongodb_action(self,deployment):
        '''
        handle all database action insert data delete backup and restore
        :param deployment: standalone replicaset or sharding
        :return:OK -1
        '''
        my_student =student_main.student()
        while True:
            os.system("clear")
            print " a - Add  new student "
            print " d - Delete all students "
            print " b - Backup db "
            print " r - Restore db "
            print " i - Insert all student"
            print " q - Return to main menu \n"
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
                    subprocess.call(shlex.split('{} {} {}'.format("mongo", "--eval", "db.fsyncLock()")))
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
                    #for each shard backup his secondary
                    db_log.debug( "dump shard 1 port {}".format(self.SHARD_1_SEONDARY_PORT_37018))
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.SHARD_1_SEONDARY_PORT_37018,
                                                self.SHARD_1_DUMP_PATH)
                    time.sleep(2)
                    db_log.debug("dump shard 2 port {}".format(self.SHARD_2_SEONDARY_PORT_47018))
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.SHARD_2_SEONDARY_PORT_47018,
                                                self.SHARD_2_DUMP_PATH)
                    time.sleep(2)
                    db_log.debug( "dump shard 3 port {}".format(self.SHARD_3_SEONDARY_PORT_57018))
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.SHARD_3_SEONDARY_PORT_57018,
                                                self.SHARD_3_DUMP_PATH)
                    time.sleep(2)
                    #backup config server
                    db_log.debug( "dump config server  port {}".format(self.SHARD_CONFIG_SERVER_PORT_57040))
                    self.mongo_dump_and_restore(self.REPLICASET_DUMP_PATH,
                                                self.LOCALHOST,
                                                self.SHARD_CONFIG_SERVER_PORT_57040,
                                                self.CONFIG_SERVER_DUMP_PATH)
                    self.start_blancer()
                else:
                    db_log.debug( "not valid deployment")
                    exit(1)
            elif user_choice == 'r':
                if deployment =="standalone":
                   self.mongo_dump_and_restore(self.STANDALONE_RESTORE_PATH,
                                               self.LOCALHOST,
                                               self.STANDALONE_PORT_27017,
                                               self.STANDALONE_DUMP_FILE_PATH)
                elif deployment =="replicaset":
                    db_log.debug( "replica set restore parameters {} {} {} {}".format(self.REPLICASET_RESTORE_PATH,
                                                                              self.LOCALHOST,
                                                                              self.REPLICASET_PRIMARY_PORT_27017,
                                                                              self.REPLICASET_DUMP_FILE_PATH))
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
                    db_log.error(" Error not valid deployment")
                    exit(1)
            elif user_choice == 'd':
                my_student.delete_student_collection()
            elif user_choice == 'i':
                my_student.insert_data_to_student_collection()
            else:
                db_log.debug( "you did not choose from the above -{} error {} \n".format(user_choice,student_main.ERR_WRONG))
                time.sleep(5)

        return 1

