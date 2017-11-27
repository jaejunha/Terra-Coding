# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
# Create your views here.
import hashlib
import datetime # for datetime filed
import pymysql # For External SQL Connection
from django.views.decorators.csrf import csrf_exempt

ERR_NO_SESSION_ID = 0x10
ERR_ROOT_ACCESSING = 0x20
ERR_NO_DABABASE = 0x30

MYSQL_ADMIN_ID = 'root'; MYSQL_ADMIN_PASSWD = '1234';
MYSQL_ADMIN_DB = 'mysql'; MYSQL_CHAR_SET = 'utf8';

@csrf_exempt
def vdbIndex(request):
    # Session ID check routine
    try:
        request.session['number']
    except:
        token = {'ReDirectURL': '/terra', 'ERR_CODE': ERR_NO_SESSION_ID}
        return render(request, 'coding/templates/error.html', token)
    owner_id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest())

    print '@@@@@@@@@@@@ OWNER ID [%s]' % owner_id
    # Establish connection between python and mysql __ START __
    root_connection = pymysql.connect(host='localhost', user=MYSQL_ADMIN_ID, password=MYSQL_ADMIN_PASSWD,
                       db=MYSQL_ADMIN_DB, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()


    row = str(VDB.objects.filter(owner_id = owner_id).first())
    result = ''
    if row == owner_id:
        sql = "SELECT TABLE_NAME, UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = '_%s';" % request.session['number']
        (status, result)= do_sql_commit(sql, root_connection, curs, "GET_SELECT_ALL")
        if status != '':
            print status
            return vdbIndex(request)
    else:
        VDB(owner_id=owner_id).save()
        create_external_vdb(request, root_connection, curs)

    try:
        curs.close()
    except:
        print 'Error[curs, already closed?]'
    try:
        root_connection.close()
    except:
        print 'Error[root_connection, already closed?]'

    token = {'result': result}
    return render(request, 'vdb/templates/index.html', token)

'''
@ Called from : vdbIndex
@ Function : create DATABASE of mysql for a user & Grant the privileges to user
'''
@csrf_exempt
def create_external_vdb(request, root_connection, curs):

    # Make information for external database __ START __
    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()) # make _passwd using MD5 hashing

    #delete_external_user_test(request, _id, databaseName)

    # Create User __START__
    sql = "create database _%s" % (databaseName)
    (status, result) = do_sql_commit(sql, root_connection, curs, "CREATE VDB")
    if status != '':
        return

    # Create external database's user & password
    sql = "create user '%s'@'%%' identified by '%s'" % (_id, _passwd)
    (status, result) = do_sql_commit(sql, root_connection, curs, "CREATE USER")
    if status != '':
        return

    # Set privileges for none super-user
    sql = "grant all privileges on _%s.* to %s@'%%' identified by '%s'; flush privileges;" % (databaseName, _id, _passwd)
    (status, result) = do_sql_commit(sql, root_connection, curs, "GRANT PRIVILEGES")
    if status != '':
        return

    return

@csrf_exempt
def createTable(request):
    operation = request.POST.get('operation', '')
    table_name = request.POST.get('table_name', '')

    if operation == 'createTable':

        # Extract one or multiple column name
        column_data = []
        for key, values in request.POST.lists():
            print '@KEY ===> %s ||| %s' % (key, values)
            if key == 'csrfmiddlewaretoken' or key == 'operation' or key == 'submit' or key == 'table_name':
                continue
            column_data = values

        create_external_table(request, table_name, column_data)
        try:
            owner_id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest())
        except:
            token = {'ReDirectURL': '/terra', 'ERR_CODE': ERR_NO_SESSION_ID}
            return render(request, 'coding/templates/error.html', token)

        return vdbIndex(request)

    token = {'table_name': table_name}
    return render(request, 'vdb/templates/createTable.html', token)

@csrf_exempt
def deleteTable(request):
    tableName = request.POST.get('tableName', '')
    tableName = tableName.replace('\n', ''); tableName = tableName.replace('\r', '');

    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='localhost', user=_id, password=_passwd,
                       db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    sql = "DROP table %s" % (tableName)
    (status, result) = do_sql_commit(sql, root_connection, curs, "DROP Table")
    if status != '':
        return

    curs.close()
    root_connection.close()
    return vdbIndex(request)

@csrf_exempt
def updateTable(request):

    return

@csrf_exempt
def viewTable(request):
    tableName = request.POST.get('tableName', '')
    # Extract user information and Create database information
    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='localhost', user=_id, password=_passwd,
                       db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    # Get Column name of Table __START__
    sql = "SHOW FIELDS FROM %s;" % (tableName)
    (status, columns)= do_sql_commit(sql, root_connection, curs, "GET_COLUMN_NAME")
    if status != '':
        print status
        return vdbIndex(request)

    # Get list of Table __START__
    sql = "select * from %s" % (tableName)
    (status, result)= do_sql_commit(sql, root_connection, curs, "GET_SELECT_ALL")
    if status != '':
        print status
        return vdbIndex(request)

    token = {'columns': columns, 'result': result }
    return render(request, 'vdb/templates/viewTable.html', token)


def create_external_table(request, _table_name, _column_data):
    tableName = _table_name; columnData = _column_data; # For Readability

    # Extract user information and Create database information
    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='localhost', user=_id, password=_passwd,
                       db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    # Assemble sql syntax from web request
    print '@@@@@ TABLE NAME [%s] ' % tableName
    sql = "CREATE TABLE %s (" % (tableName)
    for value in columnData:
        sql += " %s VARCHAR(30) ," % (value)
    sql += ");"; sql = sql.replace(',)', ')');

    print "sql syntax ===> %s ........." % sql

    (status, result) = do_sql_commit(sql, root_connection, curs, "CREATE TABLE")
    if status != '':
        return

    output = root_connection.commit()
    print output

    curs.close()
    root_connection.close()
    return

# This function is test function and will be updated.
def delete_external_user_test(request, _id, databaseName):
    root_connection = pymysql.connect(host='localhost', user=MYSQL_ADMIN_ID, password=MYSQL_ADMIN_PASSWD,
                       db=MYSQL_ADMIN_DB, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    # clean up user information
    sql = "DROP USER '%s'@'%%';" % _id
    (status, result) = do_sql_commit(sql, root_connection, curs, "DEL FROM")
    if status != '':
        return
    # drop database
    sql = "drop database _%s" % databaseName
    (status, result) = do_sql_commit(sql, root_connection, curs, "DROP DB")
    if status != '':
        return

    curs.close()
    root_connection.close()

    return

def do_sql_commit(_sql, _root_connection, _curs, error_type='[DEFAULT]'):
    sql = _sql; root_connection = _root_connection; curs = _curs # Increase Readability

    try:
        curs.execute(sql)
    except Exception as e:
        print '*****[%s] ____> %s' % (error_type, e)
        error_type = ERR_NO_DABABASE
        return (error_type, '')

    root_connection.commit() # Real execution
    result = curs.fetchall()

    return ('', result)
