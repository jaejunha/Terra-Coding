# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from coding.models import ProjectInfo

import hashlib
import os
from os.path import abspath, dirname
from subprocess import call
from django.core.urlresolvers import reverse

FORBIDDEN_TEXT_EXTENSION = ['.pyc', '.sqlite3'] # may be white list is more efficient...
ALLOWED_IMG_EXTENSION = ['.png', '.jpg']

def printDir(request):
	fileType = []

	operation = request.POST.get('operation', '')
	directoryName = request.POST.get('dirName', '')
	directoryName = nomalize_directory_path(directoryName)
	#check_user_directory(request)

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

def sourceView(request):
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('directoryName', '')

	directoryName = nomalize_directory_path(directoryName)
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

def sourceEdit(request):
	editpath = ''
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('directoryName', '')
	operation = request.POST.get('operation', '')

	directoryName = nomalize_directory_path(directoryName)
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
		token = {'dirName': fileName, 'directoryName': directoryName, 'file_data': file_data}
		return render(request, 'coding/templates/sourceEdit.html', token)

def sourceDel(request):
	fileName = request.POST.get('selected_file', '')
	directoryName = request.POST.get('dirName', '')
	directoryName = nomalize_directory_path(directoryName)

	path = directoryName + fileName
	os.popen("rm -rf " + "'" + path + "'")
	return HttpResponseRedirect('/coding/printDir.html')

def createNewFile(request):
	directoryName = request.POST.get('dirName', '')
	fileName = request.POST.get('fileName', '')
	operation = request.POST.get('operation', '')

	directoryName = nomalize_directory_path(directoryName)

	if operation == 'file':
		if fileName == '':
			fileName = 'temp.c'

		path = directoryName + fileName
		f = open(path, 'w')
		f.write('')
		f.close()

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
	directoryName = nomalize_directory_path(directoryName)

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

def nomalize_directory_path(_dirName):
	if _dirName == '': # PREVENT __EMPTY SET ERROR__
		_dirName = os.popen('pwd').read()
	if _dirName[-1] != '/': # PREVENT __DUPLICATED SLASH ERROR__
		_dirName += '/'
	_dirName = _dirName.replace('\n', '') # PRVENT __ENCODING ERROR__
	_dirName = _dirName.replace('\r', '')
	return _dirName

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

'''
def check_user_directory(obj):
	_query = ''
	_number = obj.session['number']
	_name = obj.session['name']

	#<====[ EXCEPTION HANDLER ]====>
	if _number == '' or _name == '':
		print '[#ERR] __check_user_directory()__: session info is NULL'
		return "ERR:NULL"
	#<============================>

	dirKey = _number + _name
	dirKey = dirKey.encode('utf-8')
	directoryName = hashlib.md5(dirKey).hexdigest()

	try:
		_query = ProjectInfo.objects.get(student_number = _number)
	except ProjectInfo.DoesNotExist:
		ProjectInfo(student_number = _number, student_name = _name, private_directory = directoryName)
		saveDirectory = nomalize_directory_path(os.popen('pwd').read()) + 'coding/user_source/' + directoryName
		os.popen('mkdir ' + saveDirectory)
		os.chdir(saveDirectory)

	print _query

	return
'''
