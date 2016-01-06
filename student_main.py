__author__ = 'Uriel Pavlov'

import pymongo
import time
import student_manager
from random import randint
import db_action

STANDALONE_RESTORE_PATH = './standalone/mongoRestore.sh'
STANDALONE_DUMP_PATH = './standalone/mongoDump.sh'
REPLICASET_RESTORE_PATH = './replica-set/mongoRestore.sh'
REPLICASET_DUMP_PATH = './replica-set/mongoDump.sh'
INIT_REPLICA_PATH = './script/init_replicaset.sh'

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


def generate_student_course_and_score():
    courses =["Algorithms","Java","Python","C++","Machine Learning"]
    course_doc ={}
    number_of_course = len(courses)
    for i in range(0,number_of_course):
        course =courses[i]
        score = randint(25,100)
        doc = {course:score}
        course_doc.update(doc)
    return course_doc

def insert_data_to_student_collection():
    with open("test.txt") as f:
        for line in f.readlines():
            student_id =randint(10000,99999)
            name= line.split(" ")
            f_name =name[0]
            l_name =name[1]
            print "student first name is {} last name {}".format(f_name,l_name)
            course = generate_student_course_and_score()
            doc = {"student_id":student_id,"first_name":f_name ,"last_name":l_name,"course":course}
            add_student(doc)

def add_student(doc):
    for retry in range (4):
            try:
                students=student_manager.student_collection("college","localhost")
                students.insert_students(doc)
                print "Inserted Document: "
                time.sleep(.1)
                break
            except pymongo.errors.AutoReconnect as e:
                print "Exception ",type(e), e
                print "Retrying.."
                time.sleep(5)
            except pymongo.errors.DuplicateKeyError as e:
                print "duplicate..but it worked"
                break

def delete_student_collection():
    students=student_manager.student_collection("college","localhost")
    students.delete_students({})
    
def get_student():
    students=student_manager.student_collection("college","localhost")
    res =students.get_students()
    return res

def get_student_from_replicaset(port):
    students=student_manager.student_collection("college","localhost",port)
    res =students.get_students()
    return res

def main_loop():
    while True:
        print " sa          - standalone"
        print " r           - replica-set "
        print " s           - sharding "
        print " q           - quit "
        user_choice = raw_input("Enter choice: ")
        if user_choice == 'q':
            break
        elif user_choice == 'sa':
            db_action.initiate_standalone()
            db_action.mongodb_action(STANDALONE)
        elif user_choice == 'r':#'replicaset':
            db_action.initiate_replicaset()
            db_action.mongodb_action(REPLICASET)
        elif user_choice == 's':
            db_action.initiate_sharding()
            db_action.mongodb_action(SHARDING)
        else:
            print "I don't know how to {}".format(user_choice)
            time.sleep(1)
            print ""

if __name__ == "__main__":
    main_loop()
























