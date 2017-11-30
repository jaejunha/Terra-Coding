# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

# DJANGO FAMILY
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.db import connection

from coding.models import ProjectInfo
from django.views.decorators.csrf import csrf_exempt

# DEFAULT FAMILY
import pymysql
import hashlib
import os
import threading
from os.path import abspath, dirname
from subprocess import call

# to get problem db
import sys
sys.path.insert(0,'..')
from problem.models import *

FORBIDDEN_TEXT_EXTENSION = ['.pyc', '.sqlite3'] # may be white list is more efficient...
ALLOWED_IMG_EXTENSION = ['.png', '.jpg']
ERR_NO_SESSION_ID = 0x10; ERR_ROOT_ACCESSING = 0x20;
ERR_SECURITY_BREACH = 0x30;

@csrf_exempt
def solveProblem(request):
	problem_no = request.POST.get('problem_no',0)

	result = Problem.objects.filter(no = problem_no)
	token = {'problem_name': result[0].name, 'problem_desc': result[0].desc}
	response = render(request, 'coding/templates/solveProblem.html',token)
	response.set_cookie('problem_no', problem_no)
	return response

@csrf_exempt
def solveEdit(request):
	code = ''
	result = ''
	if request.POST.get('operation','') == 'Write':
		code = request.POST.get('edit_data', '')
		f = open('test.c','w')
		f.write(code)
		f.close()
		gcc_compile_command = "gcc -o test test.c 2> error"
		os.popen(gcc_compile_command)
		result = os.popen("cat error").read()
		#have error
		if result.find('error')>=0:
			os.popen("rm test.c test error")
			token = {'code': code, 'result':result}
			return render(request, 'coding/templates/solveEdit.html',token)
		else:
			problem_no = request.COOKIES.get('problem_no')
			result = Solution.objects.all()
			for r in result:
				if int(r.sNo.no) == int(problem_no):
					if os.popen('echo "'+r.ex+'\n" | ./test').read() != r.sol :
						result = 'Wrong Answer'
						os.popen("rm test.c test error")
						token = {'code': code, 'result':result}
						return render(request, 'coding/templates/solveEdit.html',token)
			result = 'Correct Answer'
			os.popen("rm test.c test error")
	token = {'code': code, 'result':result}
	return render(request, 'coding/templates/solveEdit.html',token)

def printProblem(request):
	result = Problem.objects.filter()
        list = []
        for r in result:
                list.append((str(r.no),r.name,r.desc))

        token = {'list': list}

        return render(request, 'coding/templates/printProblem.html', token)


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

	# __ FOR FILE DATE __START__ #
	command = "ls -l " + "'" + directoryName + "'"  + " | awk '{print $6, $7, $8}'"
	fileDate = os.popen(command).read().split('\n')[1:-1]

	# __ EXTENSION FILTER IS ON __START__#
	if operation == 'categorization':
		project_attr = request.POST.get('project_attribute', '')
		if project_attr == 'C_Lang':
			fileInfo = make_file_info(fileType, fileName, fileDate, 'C')
		elif project_attr == 'CPP_LANG':
			fileInfo = make_file_info(fileType, fileName, fileDate, 'CPP')
		elif project_attr == 'Java_Lang':
			fileInfo = make_file_info(fileType, fileName, fileDate, 'JAVA')
		elif project_attr == 'Python_Lang':
			fileInfo = make_file_info(fileType, fileName, fileDate, 'PYTHON')
		if project_attr == 'ALL':
			fileInfo = make_file_info(fileType, fileName, fileDate, 'NULL')
	else:
		fileInfo = make_file_info(fileType, fileName, fileDate, 'NULL')

	rootDirectory = "./userDirectory/" + request.session['Directory'] + '/'
	#TEST code
	print os.popen('ls -la').read()
	isTopDirectory = 'false'
	if directoryName == rootDirectory:
		isTopDirectory = 'true'

	token = {'fileInfo': fileInfo, 'dirName': directoryName, 'isTop': isTopDirectory}
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
	response = render(request, 'coding/templates/sourceView.html', token)
	response.set_cookie('fileName', fileName)
	response.set_cookie('directoryName', directoryName)
	return response
#	return render(request, 'coding/templates/sourceView.html', token)

@csrf_exempt
def sourceEdit(request):
	editpath = ''
	fileName = request.COOKIES.get('fileName')
	directoryName = request.COOKIES.get('directoryName')
	operation = request.POST.get('operation', '')
	check_db_syntax = request.POST.get('check_db_syntax', '')

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

		# Save a sourceFile as translated version
		if check_db_syntax != '':
			translate_edit_data = replace_psuedo_syntax_to_db_syntax(request, edit_data)
			f = open(directoryName + "." + fileName, 'w')
			f.write(translate_edit_data)
			f.close()
		else:
			os.popen("rm -rf " + "'" + directoryName + "." + fileName + "'")

#		token = {'fileName': fileName, 'directoryName': directoryName}
	#	return render(request, 'coding/templates/sourceEdit.html', token)

	# __ RENDERING CONTENTS OF FILE __START__#
	f = open(editPath, 'r')
	file_data = f.read()
	f.close()
	token = {'fileName': fileName, 'directoryName': directoryName, 'file_data': file_data}
	return render(request, 'coding/templates/sourceEdit.html', token)

@csrf_exempt
def sourceDel(request):
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('dirName', '')

	if ('../' in directoryName) or ('*' in directoryName) or directoryName == '/':
		token = {'ReDirectURL': '/terra', 'ERR_CODE': ERR_SECURITY_BREACH}
		return render(request, 'coding/templates/error.html', token)

	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)

	path = directoryName + fileName
	os.popen("rm -rf " + "'" + path + "'")
	return printDir(request)

@csrf_exempt
def renameFile(request):
	fileName = request.POST.get('fileName', '')
	newFileName = request.POST.get('newFileName', '')
	directoryName = request.POST.get('dirName', '')

	if ('../' in directoryName) or ('*' in directoryName) or directoryName == '/':
		token = {'ReDirectURL': '/terra', 'ERR_CODE': ERR_SECURITY_BREACH}
		return render(request, 'coding/templates/error.html', token)

	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)

	path = directoryName + fileName
	os.popen("mv " + "'" + path + "' " + directoryName + newFileName)
	return printDir(request)


@csrf_exempt
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

	elif operation == 'directory':
		if fileName == '':
			fileName = '_temp_'
		mutable = request.POST._mutable
		request.POST._mutable = True
		path = directoryName + fileName
		os.popen('mkdir ' + path)
		request.POST['operation'] = ''

	elif operation == 'upload':
		status = do_file_upload(request, directoryName)
		if status == 'S':
			print "SUCEED!"
		else:
			print "FAILED!"

	post = request.POST.copy()
	post['dirName'] = directoryName
	request.POST = post
	return printDir(request)

# Connector for multiple langunage
@csrf_exempt
def compiler_connector(request):
	operation = request.POST.get('operation', '')
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('dirName', '')
	(directoryName, status) = normalize_directory_path(request, directoryName)
	if status == ERR_NO_SESSION_ID or status == ERR_ROOT_ACCESSING:
		token = {'ReDirectURL': '/terra', 'ERR_CODE': status}
		return render(request, 'coding/templates/error.html', token)

	if operation != 'directory':
		extension = os.path.splitext(fileName)[1]
		if extension == '.c' or extension == '.C':
			(result, status, directoryName) = do_compile_c_language(operation, fileName, directoryName)
		elif extension == '.java' or extension == '.JAVA':
			(result, status, directoryName) = do_compile_java_language(operation, fileName, directoryName)
		elif extension == '.py' or extension == '.PY':
			(result, status, directoryName) = do_compile_python_language(operation, fileName, directoryName)
		else:
			result = "out of service :)"
			status = 'F'

	else:
		extension = '.c' # Preventing error....
		(result, status, directoryName) = do_compile_c_language(operation, fileName, directoryName)

	django_execute_path = os.popen('pwd').read().replace('\n', '')
	django_execute_path = django_execute_path.replace('\r', '')
	wettyURL = extension + '@' + directoryName + '@' + fileName + '@' + django_execute_path
	wettyURL = wettyURL.replace('/', ',')

	token = {'result': result, 'status': status, 'directoryName': directoryName, 'wettyURL': wettyURL}
	return render(request, 'coding/templates/compile_res.html', token)

def do_compile_c_language(operation, fileName, directoryName):
	path = ''
	result = ''
	status = ''

	# __ COMPILE PER PROJECT UNIT __START__#
	if operation == 'directory':
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
			return ("out of service :)" , 'F', '')
		execute_command = "ls -a1 " + directoryName
		fileList = os.popen(execute_command).read().split('\n')

		for eachFile in fileList:
			if eachFile == ('.' + fileName):
				path = directoryName + '.' + fileName

	# __ GCC COMPILER & GET RESULT __START__#
	gcc_compile_command = "gcc -o " + directoryName + "/.main " + path + ' -w -I/usr/include/mysql -L/usr/local/lib/mysql -lmysqlclient ' + " 2> " + directoryName + "/.compile_message"
	result = os.popen(gcc_compile_command).read()
	result = os.popen("cat " + directoryName + "/.compile_message").read() # show a error message

	if result == '':
		status = 'S'
	else:
		status = 'F'
		try:
			index = result.index('userDirectory/')
			result = result[index + 55:]
		except:
			print 'compile error message <c> --> out of range'


	return (result, status, directoryName)

def do_compile_java_language(operation, fileName, directoryName):
	status = ''
	path = directoryName + fileName

	java_compile_command = "javac " + path + " 2> " + directoryName + "/.compile_message"
	result = os.popen(java_compile_command).read() # executable file will be created in manage.py directory
	result = os.popen("cat " + directoryName + "/.compile_message").read() # show a error message

	if result == '': # which means error is none
		status = 'S'
	else:
		status = 'F'
		try:
			index = result.index('userDirectory/')
			result = result[index + 55:]
		except:
			print 'compile error message <java> --> out of range'

	return (result, status, directoryName)

def do_compile_python_language(operation, fileName, directoryName):
	status = ''
	path = directoryName + fileName

	python_compile_command = "python -m py_compile " + path + " 2> " + directoryName + "/.compile_message"
	result = os.popen(python_compile_command).read() # executable file will be created in manage.py directory
	result = os.popen("cat " + directoryName + "/.compile_message").read() # show a error message
	os.popen("rm -rf " + path + 'c') # py + c ==> .pyc

	if result == '': # which means error is none
		status = 'S'
	else:
		status = 'F'
		try:
			index = result.index('userDirectory/')
			result = result[index + 55:]
		except:
			print 'compile error message <python> --> out of range'

	return (result, status, directoryName)

def errReDirection(request, ReDirectURL):
	if ReDirectURL == '': # __ PREVENT EMPTY SET ERROR ___ #
		ReDirectURL = '/terra'
	token = {'ReDirectURL': ReDirectURL}
	return render(request, 'coding/templates/error.html', token)

def make_file_info(_fileType, _fileName, _fileDate, _filter):
	row = [] # [filetype, filename]
	output = [] # it would be 2D array --- [ [filetype_1, filename_1], [filetype_2, filename_2] ]

	# Exception Handler
	if _fileType == '' or _fileName == '' or _fileDate == '':
		print '[#ERR] __make_file_info()__: filetype or filename or fileDate is NULL'
		return "ERR:NULL"
	if len(_fileType) != len(_fileName) != len(_fileDate):
		print '[#ERR] __make_file_info()__: length of array of filetype and filename is not equal'
		return "ERR:LENGTH"

	# __ MAKE 2D LIST __START__#
	MAX = len(_fileType)
	for i in range(0, MAX):
		if _fileType[i] == '-': # case of file
			extension = os.path.splitext(_fileName[i])[1].lower()
			row.append(extension)
		else: # case of directory or other things
			row.append(_fileType[i])
		row.append(_fileName[i])
		row.append(_fileDate[i])
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
		elif _filter == 'JAVA':
			FILTER.append('.java')
			FILTER.append('.class')
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
	except:  # when there is no session['Directory'] value.
		return (_currentDirectory, ERR_NO_SESSION_ID)

	rootDirectory = "./userDirectory/" + request.session['Directory'] + '/'

	curLen = len(_currentDirectory)
	rootLen = len(rootDirectory)
	if curLen <= rootLen:
		return (rootDirectory, 'Normal')

	return (_currentDirectory, 'Normal')

def normalize_directory_path(request, _dirName):
	if _dirName == '' or _dirName == '.': # PREVENT __EMPTY SET ERROR__
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

def replace_psuedo_syntax_to_db_syntax(request, _data):
	# Make database information
	hostName = "\"localhost\""
	databaseName = "\"_" + str(request.session['number']) + "\""
	databaseName = databaseName.replace('\r', ''); databaseName = databaseName.replace('\n', ''); # Normalize Database Name
	userName = "\"" + str(hashlib.md5(request.session['number']+request.session['Directory']).hexdigest())  + "\""
	userPass = "\"" + str(hashlib.md5(request.session['number']).hexdigest())  + "\""

	_data = _data.replace('__DB_HOST__', hostName)
	_data = _data.replace('__DB_USER__', userName)
	_data = _data.replace('__DB_PASS__', userPass)
	_data = _data.replace('__DB_NAME__', databaseName);

	return _data

'''
def start_wetty_server():
	print '[WETTY] thread running.....'
	execute_command = "node wetty/app.js | tee /dev/null | head"
	result = os.popen(execute_command).read()
	print 'Running wetty-----...... [%s]' % result
	return

t1 = threading.Thread(target=start_wetty_server, args=())
t1.daemon = True
t1.start()
'''
