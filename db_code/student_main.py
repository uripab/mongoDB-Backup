__author__ = 'Uriel Pavlov'

import pymongo
import time
import student_manager
from random import randint
import db_action
from log_manager import db_log

class student(object):
    '''
    class to handle student operation
    '''
    def __init__(self):
        self.courses =["Algorithms","Java","Python","C++","Machine Learning"]
        self.STANDALONE ="standalone"
        self.REPLICASET ="replicaset"
        self.SHARDING ="sharding"

    def generate_student_course_and_score(self):
        '''
        genarate student firs and last name from names.txt file course from self.courses
        score and student_id -random
        '''
        course_doc ={}
        number_of_course = len(self.courses)
        for i in range(0,number_of_course):
            course =self.courses[i]
            score = randint(25,100)
            doc = {course:score}
            course_doc.update(doc)
        return course_doc

    def insert_data_to_student_collection(self):
        with open("test.txt") as f:
            for line in f.readlines():
                student_id =randint(10000,99999)
                name= line.split(" ")
                f_name =name[0]
                l_name =name[1]
                print "student first name is {} last name {}".format(f_name,l_name)
                course = self.generate_student_course_and_score()
                doc = {"student_id":student_id,"first_name":f_name ,"last_name":l_name,"course":course}
                self.add_student(doc)

    def add_student(self,doc):
        '''
        add one document to student collection
        :param doc: -json object to insert to student collection
        '''
        for retry in range (4):
            try:
                students=student_manager.student_collection("college","localhost")
                students.insert_students(doc)
                db_log.debug( "Inserted Document: ")
                time.sleep(.1)
                break
            except pymongo.errors.AutoReconnect as e:
                db_log.error("Exception ",type(e), e)
                db_log.debug( "Retrying..")
                time.sleep(5)
            except pymongo.errors.DuplicateKeyError as e:
                db_log.debug( "duplicate..but it worked")
                break

    def delete_student_collection(self):
        '''
        delete all students from  students collection
        '''
        students=student_manager.student_collection("college","localhost")
        students.delete_students({})

    def get_student(self):
        '''
        get all student from db
        :return: list of student
        '''
        students=student_manager.student_collection("college","localhost")
        res =students.get_students()
        return res

    def get_student_from_replicaset(self,port):
        '''
        get student data from specific server in the replica set
        :param port:server port
        :return: list of student
        '''
        students=student_manager.student_collection("college","localhost",port)
        res =students.get_students()
        return res

def main_loop():
    '''
    program start point create and init the enviroments
    '''
    action =db_action.database_action()
    while True:
        print " sa          - standalone"
        print " r           - replica-set "
        print " s           - sharding "
        print " q           - quit "
        user_choice = raw_input("Enter choice: ")
        if user_choice == 'q':
            break
        elif user_choice == 'sa':
            action.initiate_standalone()
            action.mongodb_action(action.STANDALONE)
        elif user_choice == 'r':#'replicaset':
            action.initiate_replicaset()
            action.mongodb_action(action.REPLICASET)
        elif user_choice == 's':
            action.initiate_sharding()
            action.mongodb_action(action.SHARDING)
        else:
            print "I don't know how to {}".format(user_choice)
            time.sleep(1)
            print ""

if __name__ == "__main__":
    main_loop()
























