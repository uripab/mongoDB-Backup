#!/usr/bin/python
import json
import bottle
from bottle import route, run, view,template
import sys
sys.path.append("/home/uripab/mongo_backup")
import bu_students

student_column =["student_id","first_name","last_name","course"]

@route('/')
@route('/Standalone')
@view('student')
def standalone():
    data=bu_students.get_student()
    return dict(title='students',db_type='Standalone',data=data,student_column=student_column)


@route('/Replica-set')
@view('replica-set')
def replicaset():
    primary_port = "27017"
    secendary_port = "27018"
    primary_data=bu_students.get_student_from_replicaset(primary_port)
    secendary_data=bu_students.get_student_from_replicaset(secendary_port)
    return dict(title='Replica-set',db_type='Replica-set',data=primary_data,secendary_data =secendary_data,
                student_column=student_column,primary_port=primary_port,secendary_port=secendary_port)


@route('/Sharding')
@route('/Shard/1')
@view('sharding')
def sharding():
    primary_port = "37017"
    secendary_port = "37018"
    primary_data=bu_students.get_student_from_replicaset(primary_port)
    secendary_data=bu_students.get_student_from_replicaset(secendary_port)
    return dict(title='Shard-1',db_type='Shardingt',data=primary_data,secendary_data =secendary_data,
                student_column=student_column,primary_port=primary_port,secendary_port=secendary_port)


@route('/Shard/2')
@view('sharding')
def sharding():
    primary_port = "47017"
    secendary_port = "47018"
    primary_data=bu_students.get_student_from_replicaset(primary_port)
    secendary_data=bu_students.get_student_from_replicaset(secendary_port)
    return dict(title='Shard-2',db_type='Shardingt',data=primary_data,secendary_data =secendary_data,
                student_column=student_column,primary_port=primary_port,secendary_port=secendary_port)

@route('/Shard/3')
@view('sharding')
def sharding():
    primary_port = "57017"
    secendary_port = "57018"
    primary_data=bu_students.get_student_from_replicaset(primary_port)
    secendary_data=bu_students.get_student_from_replicaset(secendary_port)
    return dict(title='Shard-3',db_type='Shardingt',data=primary_data,secendary_data =secendary_data,
                student_column=student_column,primary_port=primary_port,secendary_port=secendary_port)

run(host='0.0.0.0', port=8889, debug=True)


