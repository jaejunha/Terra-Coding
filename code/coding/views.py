# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

# DJANGO FAMILY
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.db import connection

from coding.models import ProjectInfo
from django.views.decorators.csrf import csrf_exempt

# DEFAULT FAMILY
import pymysql
import hashlib
import os
from os.path import abspath, dirname
from subprocess import call

FORBIDDEN_TEXT_EXTENSION = ['.pyc', '.sqlite3'] # may be white list is more efficient...
ALLOWED_IMG_EXTENSION = ['.png', '.jpg']
ERR_NO_SESSION_ID = 0x10
ERR_ROOT_ACCESSING = 0x20

@csrf_exempt
def printDir(request):
	fileType = []
	operation = request.POST.get('operation', '')
	directoryName = request.POST.get('dirName', '')

	if directoryName ==	 '':
		directoryName = './'

	# __ NORMALIZE DIRECTORY PATH & PREVENT ERROR  __START__#
	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)

	# __ REDIRECT BETWEEN DIRECTORIES __START__#
	if operation == 'ReDirect':
		folderName = request.POST.get('folder', '')
		directoryName += folderName

	# __ GO TO PARENT DIRECTORY __START__#
	elif operation == 'GoBack':
		index = len(directoryName) - 2
		while index > 0: # Find a parent path until meeting '/' character
			if directoryName[index] == '/':
				break
			index = index - 1
		directoryName = directoryName[:index]

	# __ ROOT DIRECTORY RESTRICTION __START__#
	(directoryName, status)= block_top_directory(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)

	# __ -L OPTION FOR FILE TYPE __START__#
	command = 'ls -l ' + "'" + directoryName + "'"
	result = os.popen(command).read().split('\n')[1:-1] # except first line(due to total info for ls command) & split by '\n'
	for _type in result:
		fileType.append(_type[0])

	# __ -1 OPTION FOR FILE NAME __START__#
	command = 'ls -1 ' + "'" + directoryName + "'"
	fileName = os.popen(command).read().split('\n')[:-1]

	# __ EXTENSION FILTER IS ON __START__#
	if operation == 'categorization':
		project_attr = request.POST.get('project_attribute', '')
		if project_attr == 'C_Lang':
			fileInfo = make_file_info(fileType, fileName, 'C')
		elif project_attr == 'CPP_LANG':
			fileInfo = make_file_info(fileType, fileName, 'CPP')
		elif project_attr == 'Python_Lang':
			fileInfo = make_file_info(fileType, fileName, 'PYTHON')
		if project_attr == 'ALL':
			fileInfo = make_file_info(fileType, fileName, 'NULL')
	else:
		fileInfo = make_file_info(fileType, fileName, 'NULL')

	token = {'fileInfo': fileInfo, 'dirName': directoryName}
	return render(request, 'coding/templates/printDir.html', token)

@csrf_exempt
def sourceView(request):
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('directoryName', '')

	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)
	extension = os.path.splitext(fileName)[1]
	viewPath = directoryName + fileName

	# __ BLOCKING BINARY FILE __START__#
	for _compare in FORBIDDEN_TEXT_EXTENSION:
		if _compare == extension:
			token = {'file_data': "This is Raw format.... Mate :)", 'fileName': fileName, 'directoryName': directoryName, 'service_type': "raw"}
			return render(request, 'coding/templates/sourceView.html', token)

	# __ HANDLING IMAGE FILE __START__#
	for _compare in ALLOWED_IMG_EXTENSION:
		if _compare == extension:
			token = {'file_data': "NONE", 'viewPath': viewPath, 'fileName': fileName, 'directoryName': directoryName, 'service_type': "img"}
			return render(request, 'coding/templates/sourceView.html', token)

	viewPath = directoryName + fileName
	f = open(viewPath, 'r')
	file_data = f.read()
	f.close()

	token = {'file_data': file_data, 'fileName': fileName, 'directoryName': directoryName, 'service_type': "text"}
	return render(request, 'coding/templates/sourceView.html', token)

@csrf_exempt
def sourceEdit(request):
	editpath = ''
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('directoryName', '')
	operation = request.POST.get('operation', '')

	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)
	editPath = directoryName + fileName

	# __ ALTER CONTENTS OF FILE __START__#
	if operation == 'Write':
		edit_data = request.POST.get('edit_data', '')
		f = open(editPath, 'w')
		f.write(edit_data)
		f.close()
		token = {'fileName': fileName, 'directoryName': directoryName}
		return sourceView(request)

	# __ RENDERING CONTENTS OF FILE __START__#
	else:
		f = open(editPath, 'r')
		file_data = f.read()
		f.close()
		token = {'fileName': fileName, 'directoryName': directoryName, 'file_data': file_data}
		return render(request, 'coding/templates/sourceEdit.html', token)

def sourceDel(request):
	fileName = request.POST.get('selected_file', '')
	directoryName = request.POST.get('dirName', '')
	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)

	path = directoryName + fileName
	os.popen("rm -rf " + "'" + path + "'")
	return HttpResponseRedirect('/coding/printDir.html')

def createNewFile(request):
	directoryName = request.POST.get('dirName', '')
	fileName = request.POST.get('fileName', '')
	operation = request.POST.get('operation', '')

	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)

	if operation == 'file':
		if fileName == '':
			fileName = 'temp.c'

		path = directoryName + fileName
		f = open(path, 'w')
		f.write('')
		f.close()

		post = request.POST.copy()
		post['fileName'] = fileName
		post['directoryName'] = directoryName
		request.POST = post
		print request.POST['fileName']

	elif operation == 'upload':
		status = do_file_upload(request, directoryName)
		return printDir(request)

	'''elif operation == 'directory': ===> EXTERMERLY DANGEROUS
		if fileName == '':
			fileName = '_temp_'
		mutable = request.POST._mutable
		request.POST._mutable = True
		path = directoryName + fileName
		os.popen('mkdir ' + path)
		request.POST['operation'] = ''
		return printDir(request)'''

	return sourceEdit(request)

def do_compile_c_language(request):
	path = ''
	result = ''
	status = ''
	operation = request.POST.get('operation', '')
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('dirName', '')
	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)

	# __ COMPILE PER PROJECT UNIT __START__#
	if operation == 'ALL':
		command = 'ls -1 ' + directoryName
		allName = os.popen(command).read().split('\n')
		fileName_c = get_all_c_files_name(allName)
		for _file in fileName_c:
			path += (' ' + directoryName + _file)

	# __ COMPILE PER FILE UNIT __START__#
	elif operation == 'selected': # Compile on a file unit
		extension = os.path.splitext(fileName)[1]
		path = directoryName + fileName
		if extension != '.c':
			token = {'result': "out of service format :)" , 'status': 'F'}
			return render(request, 'coding/templates/compile_res.html', token)

	# __ GCC COMPILER & GET RESULT __START__#
	gcc_compile_command = "gcc -o " + directoryName + "/main " + path + " 2> " + directoryName + "/compile_message"
	result = os.popen(gcc_compile_command).read() # executable file will be created in manage.py directory
	result = os.popen("cat " + directoryName + "/compile_message").read() # show a error message

	# __ COMPILE STATUS __START__#
	if result == '': # which means error is none
		status = 'S'
		result = os.popen(directoryName + "/main").read()
	else:
		status = 'F'

	token = {'result': result, 'status': status, 'directoryName': directoryName}
	return render(request, 'coding/templates/compile_res.html', token)

def errReDirection(request, ReDirectURL):
	if ReDirectURL == '': # __ PREVENT EMPTY SET ERROR ___ #
		ReDirectURL = '/terra'
	token = {'ReDirectURL': ReDirectURL}
	return render(request, 'coding/templates/error.html', token)

def make_file_info(_fileType, _fileName, _filter):
	output = [] # it would be 2D array --- [ [filetype_1, filename_1], [filetype_2, filename_2] ]
	row = [] # [filetype, filename]

	'''<====[ EXCEPTION HANDLER ]====>'''
	if _fileType == '' or _fileName == '':
		print '[#ERR] __make_file_info()__: filetype or filename is NULL'
		return "ERR:NULL"
	if len(_fileType) != len(_fileName):
		print '[#ERR] __make_file_info()__: length of filetype and filename is not equal'
		return "ERR:LENGTH"
	'''<============================>'''

# __ MAKE 2D LIST __START__#
	MAX = len(_fileType)
	for i in range(0, MAX):
		if _fileType[i] == '-': # case of file
			extension = os.path.splitext(_fileName[i])[1].lower()
			row.append(extension)
		else: # case of directory or other things
			row.append(_fileType[i])
		row.append(_fileName[i])
		output.append(row)
		row = []

# __ EXTENSION FILTER __START__#
	tempOut = []
	FILTER = []
	if _filter != 'NULL':
		if _filter == 'C':
			FILTER.append('.c')
			FILTER.append('.h')
		elif _filter == 'CPP':
			FILTER.append('.cpp')
			FILTER.append('.h')
		elif _filter == 'PYTHON':
			FILTER.append('.py')
			FILTER.append('.pyc')
		for _row in output:
			if _row[0] == FILTER[0] or _row[0] == FILTER[1]:
				tempOut.append(_row)
		output = tempOut

	return output

def block_top_directory(request, _currentDirectory):

	try:
		if request.session['Directory'] == '': # Session itself exists, but there is no contents.
			return (_currentDirectory, ERR_NO_SESSION_ID)
		rootDirectory = "./userDirectory/" + request.session['Directory'] + '/'
	except:  # when there is no session['Directory'] value.
		return (_currentDirectory, ERR_NO_SESSION_ID)

	curLen = len(_currentDirectory)
	rootLen = len(rootDirectory)
	if curLen < rootLen or curLen == rootLen:
		return (rootDirectory, 'Normal')

	return (_currentDirectory, 'Normal')

def normalize_directory_path(request, _dirName):
	if _dirName == '' or '.': # PREVENT __EMPTY SET ERROR__
		try:
			_dirName = "./userDirectory/" + request.session['Directory'] # Relative Path must be used.
		except:
			request.session.flush()
			return (_dirName, ERR_NO_SESSION_ID)

	if _dirName[0] == '/': # PREVENT __ ROOT ACCESSING __ FOR SECURITY
		return (_dirName, ERR_ROOT_ACCESSING)

	if _dirName[-1] != '/': # PREVENT __DUPLICATED SLASH ERROR__
		_dirName += '/'
	_dirName = _dirName.replace('\n', '') # PRVENT __ENCODING ERROR__
	_dirName = _dirName.replace('\r', '')
	return (_dirName, 'Normal')

def get_all_c_files_name(fileList):
	output = []

	for fileName in fileList:
		extension = os.path.splitext(fileName)[1]
		if extension == '.c' or extension == '.h':
			output.append(fileName)

	return output

def do_file_upload(req, _directoryName):
    if req.method == 'POST':
        if 'file' in req.FILES:
            file = req.FILES['file']
            filename = file._name

            fp = open('%s/%s' % (_directoryName, filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
            return "S"

    return "F"

def external_database_connector():
	conn = pymysql.connect(host='localhost', user='root', password='1234',
	                       db='testDB', charset='utf8')
	curs = conn.cursor()

	for i in range(1,100):
		sql = "insert into users values ('%s', '%s', '%s')" % (i,i,i)
		try:
		    curs.execute(sql)
		except curs.Error, e:
			print "MySQL Error: %s" % e

	conn.commit()
	curs.close()
	conn.close()

	return
