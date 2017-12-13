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
    owner_id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13])

    # Establish connection between python and mysql __ START __
    root_connection = pymysql.connect(host='127.0.0.1', user=MYSQL_ADMIN_ID, password=MYSQL_ADMIN_PASSWD, db=MYSQL_ADMIN_DB, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    status = ''
    # CHECK ROUTINE
    # WHETHER USER'S DATABASE EXIST.
    if status != '':
        print status
        return vdbIndex(request)

    create_external_vdb(request, root_connection, curs)

    result = ''
    sql = "SELECT TABLE_NAME, TABLE_ROWS, UPDATE_TIME FROM information_schema.tables WHERE TABLE_SCHEMA = '_%s';" % request.session['number']
    (status, result)= do_sql_commit(sql, root_connection, curs, "GET USER'S TABLE INFORMATIONS")
    if status != '':
        print status
        return vdbIndex(request)

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
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13]) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()[:13]) # make _passwd using MD5 hashing

    # Create DATABASE
    sql = "CREATE DATABASE IF NOT EXISTS _%s" % databaseName
    (status, result)= do_sql_commit(sql, root_connection, curs, "CREATE DATABASE IF NOT EXISTS")

    # Create external database's user & password
    sql = "create user '%s'@'%%' identified by '%s'" % (_id, _passwd)
    (status, result) = do_sql_commit(sql, root_connection, curs, "CREATE USER")

    # Set privileges for none super-user
    sql = "grant all privileges on _%s.* to %s@'%%' identified by '%s'; flush privileges;" % (databaseName, _id, _passwd)
    (status, result) = do_sql_commit(sql, root_connection, curs, "GRANT PRIVILEGES")

    return

@csrf_exempt
def createTable(request):
    operation = request.POST.get('operation', '')
    table_name = request.POST.get('table_name', '')

    if operation == 'createTable':

        # Extract one or multiple column name
        column_data = []
        for key, values in request.POST.lists():
            if key == 'csrfmiddlewaretoken' or key == 'operation' or key == 'submit' or key == 'table_name':
                continue
            column_data = values

        create_external_table(request, table_name, column_data)

        try:
            owner_id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13])
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
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13]) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()[:13]) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='localhost', user=_id, password=_passwd, db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    sql = "DROP table %s" % (tableName)
    (status, result) = do_sql_commit(sql, root_connection, curs, "DROP Table")
    if status != '':
        return

    curs.close()
    root_connection.close()
    return vdbIndex(request)

@csrf_exempt
def renameTable(request):
    tableName = request.POST.get('tableName', '')
    newTableName = request.POST.get('newTableName', '')

    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13]) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()[:13]) # make _passwd using MD5 hashing

    tableName = request.POST.get('tableName', '')

    root_connection = pymysql.connect(host='127.0.0.1', user=_id, password=_passwd, db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    # rename table [SR] to [DS];
    sql = "rename table %s to %s" % (tableName, newTableName)
    (status, columns)= do_sql_commit(sql, root_connection, curs, "rename table")
    if status != '':
        print status
        return vdbIndex(request)

    return vdbIndex(request)

@csrf_exempt
def updateTable(request):
    tableName = request.POST.get('tableName', '')

    # rename table [SR] to [DS];
    return


@csrf_exempt
def viewTable(request):
    tableName = request.POST.get('tableName', '')
    # Extract user information and Create database information
    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13]) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()[:13]) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='127.0.0.1', user=_id, password=_passwd, db='_'+databaseName, charset=MYSQL_CHAR_SET)
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

    token = {'columns': columns, 'result': result , 'tableName': tableName}
    return render(request, 'vdb/templates/viewTable.html', token)


def create_external_table(request, _table_name, _column_data):
    tableName = _table_name; columnData = _column_data; # For Readability

    # Extract user information and Create database information
    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13]) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()[:13]) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='127.0.0.1', user=_id, password=_passwd, db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    # Assemble sql syntax from web request
    sql = "CREATE TABLE %s (" % (tableName)
    for value in columnData:
        sql += " %s VARCHAR(30) ," % (value)
    sql += ");"; sql = sql.replace(',)', ')');

    (status, result) = do_sql_commit(sql, root_connection, curs, "CREATE TABLE")
    if status != '':
        return

    output = root_connection.commit()
    print output

    curs.close()
    root_connection.close()
    return

@csrf_exempt
def renameColumn(request):
    tableName = request.POST.get('tableName', '')
    columnName = request.POST.get('columnName', '')
    newColumnName = request.POST.get('newColumnName', '')

    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13]) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()[:13]) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='127.0.0.1', user=_id, password=_passwd, db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    sql = "alter table %s change %s %s varchar(30)" % (tableName, columnName, newColumnName)
    print sql
    (status, result) = do_sql_commit(sql, root_connection, curs, "ALTER COLUMN")
    if status != '':
        return viewTable(request)

    return viewTable(request)

@csrf_exempt
def insertColumn(request):
    tableName = request.POST.get('tableName', '')
    columnName = request.POST.get('columnName', '')
    newColumnName = request.POST.get('newColumnName', '')


    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13]) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()[:13]) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='127.0.0.1', user=_id, password=_passwd, db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    sql = "alter table %s add %s varchar(30) after %s" % (tableName, newColumnName, columnName)
    print sql
    (status, result) = do_sql_commit(sql, root_connection, curs, "INSERT COLUMN")
    if status != '':
        return viewTable(request)


    return viewTable(request)

@csrf_exempt
def deleteColumn(request):
    tableName = request.POST.get('tableName', '')
    columnName = request.POST.get('columnName', '')

    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()[:13]) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()[:13]) # make _passwd using MD5 hashing

    root_connection = pymysql.connect(host='127.0.0.1', user=_id, password=_passwd, db='_'+databaseName, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    sql = "alter table %s drop %s;" % (tableName, columnName)
    print sql
    (status, result) = do_sql_commit(sql, root_connection, curs, "DORP COLUMN")
    if status != '':
        return viewTable(request)

    return viewTable(request)

# This function is test function and will be updated.
def delete_external_user_test(request, _id, databaseName):
    root_connection = pymysql.connect(host='127.0.0.1', user=MYSQL_ADMIN_ID, password=MYSQL_ADMIN_PASSWD, db=MYSQL_ADMIN_DB, charset=MYSQL_CHAR_SET)
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
        if int(e[0]) != 1396 and int(e[0]) != 1007: # Except things...
            print '*****[%s] ____> %s' % (error_type, e)
            error_type = ERR_NO_DABABASE
            return (error_type, '')

    root_connection.commit() # Real execution
    result = curs.fetchall()

    return ('', result)
