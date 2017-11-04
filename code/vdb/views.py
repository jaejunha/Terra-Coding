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
    table = table.replace('\n', '')
    table = table.replace('\r', '')
    for _row in VDB.objects.filter(table=table):
        _row.delete()

    return
