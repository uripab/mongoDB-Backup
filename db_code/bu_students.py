__author__ = 'Uriel Pavlov'

import pymongo
import time
import student_manager
from random import randint
import subprocess
import shlex

STANDALONE_RESTORE_PATH ='./standalone/mongoRestore.sh'
STANDALONE_DUMP_PATH ='./standalone/mongoDump.sh'
LOCALHOST ='localhost'
PORT_27017 ='27017'

def mongo_dump_and_restore(path,host,port):
    print shlex.split('{} {} {}'.format(path,host ,port))
    subprocess.call(shlex.split('{} {} {}'.format(path,host ,port)))

def generate_student_course_and_score():
    courses =["Java","Python","C++","Machine Learning"]
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
            name= line.split(" ")
            f_name =name[0]
            l_name =name[1]
            print "student first name is {} last name {}".format(f_name,l_name)
            course = generate_student_course_and_score()
            doc = {"first_name":f_name ,"last_name":l_name,"course":course}
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

def main_loop():
    while True:
        print " q - quit "
        print " a - add student "
        print " d - delete students "
        print " b - backup db "
        print " r - restore db "
        print " i - insert all student"

        user_choice = raw_input("Enter choice: ")

        if user_choice == 'q':
            break

        elif user_choice == 'a':
            new_student = { }
            new_student['first_name'] = raw_input("Enter first name: ")
            new_student['last_name'] = raw_input("Enter last name: ")
            new_student['course'] = {}
            add_student(new_student)

        elif user_choice == 'b':
            mongo_dump_and_restore(STANDALONE_DUMP_PATH,LOCALHOST,PORT_27017)
        elif user_choice == 'r':
            mongo_dump_and_restore(STANDALONE_RESTORE_PATH,LOCALHOST,PORT_27017)
        elif user_choice == 'd':
            delete_student_collection()
        elif user_choice == 'i':
            insert_data_to_student_collection()
        else:
            print "I don't know how to {}".format(user_choice)
            time.sleep(1)
            print ""


if __name__ == "__main__":
    main_loop()
























