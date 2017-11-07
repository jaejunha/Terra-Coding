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

MYSQL_ADMIN_ID = 'root'; MYSQL_ADMIN_PASSWD = '1234';
MYSQL_ADMIN_DB = 'mysql'; MYSQL_CHAR_SET = 'utf8';

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

def createTable(request):
    operation = request.POST.get('operation', '')

    if operation == 'createTable':
        table_name = request.POST.get('table_name', '')

        # Extract one or multiple column name
        column_data = []
        for key, values in request.POST.lists():
            if key == 'csrfmiddlewaretoken' or key == 'operation' or key == 'submit' or key == 'table_name':
                continue
            column_data.append([key, values[0]])

        create_external_table(request, table_name, column_data)
        try:
            owner_id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest())
        except:
            token = {'ReDirectURL': '/terra', 'ERR_CODE': ERR_NO_SESSION_ID}
            return render(request, 'coding/templates/error.html', token)

        VDB(owner_id=str(owner_id), table=str(table_name)).save()
        return vdbIndex(request)

    token = {'result': 'test'}
    return render(request, 'vdb/templates/createTable.html', token)

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
    root_connection = pymysql.connect(host='localhost', user=MYSQL_ADMIN_ID, password=MYSQL_ADMIN_PASSWD,
                       db=MYSQL_ADMIN_DB, charset=MYSQL_CHAR_SET)
    curs = root_connection.cursor()

    # Make information for external database __ START __
    databaseName = str(request.session['number']) # make databaseName
    databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
    _id = str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest()) # make _id using MD5 hashing
    _passwd = str(hashlib.md5(request.session['number']).hexdigest()) # make _passwd using MD5 hashing

    #delete_external_user_test(request, _id, databaseName)

    # Create User __START__
    sql = "create database _%s" % (databaseName)
    status = do_sql_commit(sql, root_connection, curs, "CREATE VDB")
    if status != '':
        return

    # Create external database's user & password
    sql = "create user '%s'@'%%' identified by '%s'" % (_id, _passwd)
    status = do_sql_commit(sql, root_connection, curs, "CREATE USER")
    if status != '':
        return

    # Set privileges for none super-user
    sql = "grant all privileges on _%s.* to %s@'%%' identified by '%s'; flush privileges;" % (databaseName, _id, _passwd)
    status = do_sql_commit(sql, root_connection, curs, "GRANT PRIVILEGES")
    if status != '':
        return

    curs.close()
    root_connection.close()
    return

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

    # Exception Routine for there are no column_data
    # ----> Please implement code here

    # Assemble sql syntax from web request
    sql = "CREATE TABLE %s (" % (tableName)
    for (key, _colName) in columnData:
        sql += " %s VARCHAR(30) ," % (_colName)
    sql += ");"; sql = sql.replace(',)', ')');

    print "sql syntax ===> %s ........." % sql

    status = do_sql_commit(sql, root_connection, curs, "CREATE TABLE")
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
    status = do_sql_commit(sql, root_connection, curs, "DEL FROM")
    if status != '':
        return
    # drop database
    sql = "drop database _%s" % databaseName
    status = do_sql_commit(sql, root_connection, curs, "DROP DB")
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
        curs.close()
        root_connection.close()
        return error_type

    root_connection.commit() # Real execution

    return ''
