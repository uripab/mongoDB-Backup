#!/usr/bin/python
import json
import bottle
from bottle import route, run, view,template, request
import sys
sys.path.append("/home/uripab/mongo_backup")
import bu_students


@route('/')
@route('/Standalone')
@view('student')
def hello(name = "uri"):
    student_list =[]
    student_column=["first_name","last_name","course"]
    data=bu_students.get_student()
    for i in  data:
        print i
    return dict(name=name,title='students',db_type='Standalone',data=data,student_column=student_column)


@route('/Replicaset')
def replicaset():
    return 'REPLICA SET'

@route('/Sharding')
def sharding():
    return 'SHARDING'

run(host='0.0.0.0', port=8889, debug=True)
#run(host='localhost', port=8889, debug=True)