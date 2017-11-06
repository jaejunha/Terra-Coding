# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
# Create your views here.
import hashlib
import datetime # for datetime filed
import pymysql # For External SQL Connection

ERR_NO_SESSION_ID = 0x10
ERR_ROOT_ACCESSING = 0x20

def vdbIndex(request):
    try:
        request.session['number']
    except:
        token = {'ReDirectURL': '/terra', 'ERR_CODE': ERR_NO_SESSION_ID}
        return render(request, 'coding/templates/error.html', token)

    create_external_vdb(request)

    output = []
    owner_id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest())
    for _row in VDB.objects.filter(owner_id=owner_id):
        output.append([str(_row.table), str(_row.date)])

    token = {'result': output}
    return render(request, 'vdb/templates/index.html', token)

def createVDB(request):
    operation = request.POST.get('operation', '')

    if operation == 'createVDB':
        table_name = request.POST.get('table_name', '')

        # Extract one or multiple column name
        column_data = []
        for key, values in request.POST.lists():
            if key == 'csrfmiddlewaretoken' or key == 'operation' or key == 'submit' or key == 'table_name':
                continue
            column_data.append([key, values[0]])

        try:
            owner_id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest())
        except:
            token = {'ReDirectURL': '/terra', 'ERR_CODE': ERR_NO_SESSION_ID}
            return render(request, 'coding/templates/error.html', token)

        VDB(owner_id=str(owner_id), table=str(table_name)).save()
        return vdbIndex(request)

    token = {'result': 'test'}
    return render(request, 'vdb/templates/createVDB.html', token)

def deleteVDB(request):
    table = request.POST.get('table_name', '')
    table = table.replace('\n', ''); table = table.replace('\r', '');
    for _row in VDB.objects.filter(table=table):
        _row.delete()

    return

# it is not creating "Table", it is creating "Database for user"
# So... this check routine may added in /terra where login is successful
def create_external_vdb(request):
    # Establish connection between python and mysql __ START __
    root_connection = pymysql.connect(host='localhost', user='root', password='1234',
                       db='mysql', charset='utf8')
    curs = root_connection.cursor()

    # Make information for external database __ START __
    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()) # make _passwd using MD5 hashing

    #delete_external_user_test(request, _id, databaseName)

    #create_external_table(request, _id, _passwd, databaseName)
    # Create User __START__
    sql = "create database _%s" % (databaseName)
    try:
        curs.execute(sql)
    except Exception as e:
        if e[0] == 1007:
            print "Database already exists!"
        else:
            print "[@ERR] CREATE DATABASE [%s]" % e[1]
        curs.close()
        root_connection.close()
        return
    root_connection.commit()

    # Create external database's user & password
    sql = "create user '%s'@'%%' identified by '%s'" % (_id, _passwd)
    try:
        curs.execute(sql)
    except Exception as e:
        print "[@ERR] CREATE USER  [%s]" % e[1]
        curs.close()
        root_connection.close()
        return
    root_connection.commit()

    # Set privileges for none super-user
    sql = "grant all privileges on _%s.* to %s@'%%' identified by '%s'; flush privileges;" % (databaseName, _id, _passwd)
    try:
        curs.execute(sql)
    except Exception as e:
        print '[@ERR]___GRANT PRIVILEGES [%s]' % e[1]
        curs.close()
        root_connection.close()
        return
    root_connection.commit()


    curs.close()
    root_connection.close()
    return

def create_external_table(request, _id, _passwd, databaseName):

    root_connection = pymysql.connect(host='localhost', user=_id, password=_passwd,
                       db='_'+databaseName, charset='utf8')
    curs = root_connection.cursor()

    tableName = 'TestTable1'
    sql = "CREATE TABLE %s \
    ( _id INT PRIMARY KEY AUTO_INCREMENT, \
    name VARCHAR(32) NOT NULL, \
    belong VARCHAR(12) DEFAULT 'FOO', \
    phone VARCHAR(12) )" % (tableName)

    try:
        curs.execute(sql)
    except Exception as e:
        print "@ERR_[Create_TABLE]__%s" % e

    output = root_connection.commit()
    print output

    curs.close()
    root_connection.close()
    return

# This function is test function and will be updated.
def delete_external_user_test(request, _id, databaseName):
    root_connection = pymysql.connect(host='localhost', user='root', password='1234',
                       db='mysql', charset='utf8')
    curs = root_connection.cursor()

    # clean up user information
    sql = "DROP USER '%s'@'%%';" % _id
    try:
        curs.execute(sql)
    except Exception as e:
        print '*****[delete from] ____> %s' % e
    root_connection.commit() # Real execution

    # drop database
    sql = "drop database _%s" % databaseName
    try:
        curs.execute(sql)
    except Exception as e:
        print '[*****Drop database] ____> %s' % e
    root_connection.commit() # Real execution


    curs.close()
    root_connection.close()

    return
