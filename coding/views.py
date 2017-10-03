# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from .models import *

import os
from os.path import abspath, dirname
from subprocess import call
from django.core.urlresolvers import reverse

FORBIDDEN_TEXT_EXTENSION = ['.pyc', '.sqlite3'] # may be white list is more efficient...
ALLOWED_IMG_EXTENSION = ['.png', '.jpg']

def get_all_c_files_name(fileList):
	output = []

	for fileName in fileList:
		extension = os.path.splitext(fileName)[1]
		if extension == '.c' or extension == '.h':
			output.append(fileName)

	return output

def do_compile_c_language(request):
	path = ''
	result = ''
	status = ''
	operation = request.POST.get('operation', '')
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('dirName', '')

	directoryName = nomalize_directory_path(directoryName)

	if operation == 'ALL': # Compile on a Project unit
		command = 'ls -1 ' + directoryName
		allName = os.popen(command).read().split('\n')
		fileName_c = get_all_c_files_name(allName)
		for _file in fileName_c:
			path += (' ' + directoryName + _file)

	elif operation == 'selected': # Compile on a file unit
		extension = os.path.splitext(fileName)[1]
		path = directoryName + fileName
		if extension != '.c':
			token = {'result': "out of service format :)" , 'status': 'F'}
			return render(request, 'coding/templates/compile_res.html', token)

	gcc_compile_command = "gcc -o " + directoryName + "/main " + path + " 2> " + directoryName + "/compile_message"
	result = os.popen(gcc_compile_command).read() # executable file will be created in manage.py directory
	result = os.popen("cat " + directoryName + "/compile_message").read() # show a error message

	if result == '': # which means error is none
		status = 'S'
		result = os.popen(directoryName + "/main").read()
	else:
		status = 'F'

	token = {'result': result, 'status': status, 'directoryName': directoryName}
	return render(request, 'coding/templates/compile_res.html', token)

def createNewFile(request):
	directoryName = request.POST.get('directoryName', '')
	fileName = request.POST.get('fileName', '')

	directoryName = nomalize_directory_path(directoryName)
	if fileName == '':
		fileName = 'temp.c'

	path = directoryName + fileName
	f = open(path, 'w')
	f.write('')
	f.close()

	return sourceEdit(request)

def sourceDel(request):
	fileName = request.POST.get('selected_file', '')
	directoryName = request.POST.get('dirName', '')
	directoryName = nomalize_directory_path(directoryName)

	path = directoryName + fileName
	os.popen("rm -rf " + path)
	return printDir(request)

def sourceEdit(request):
	editpath = ''
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('directoryName', '')
	operation = request.POST.get('operation', '')

	directoryName = nomalize_directory_path(directoryName)
	editPath = directoryName + fileName

	if operation == 'Write':
		edit_data = request.POST.get('edit_data', '')
		f = open(editPath, 'w')
		f.write(edit_data)
		f.close()
		token = {'fileName': fileName, 'directoryName': directoryName}
		return sourceView(request)

	else:
		f = open(editPath, 'r')
		file_data = f.read()
		f.close()
		token = {'fileName': fileName, 'directoryName': directoryName, 'file_data': file_data}
		return render(request, 'coding/templates/sourceEdit.html', token)

def sourceView(request):
	fileName = request.POST.get('fileName', '')
	directoryName = request.POST.get('directoryName', '')

	directoryName = nomalize_directory_path(directoryName)
	extension = os.path.splitext(fileName)[1]
	viewPath = directoryName + fileName

	for _compare in FORBIDDEN_TEXT_EXTENSION:
		if _compare == extension:
			token = {'file_data': "This is Raw format.... Mate :)", 'fileName': fileName, 'directoryName': directoryName, 'service_type': "raw"}
			return render(request, 'coding/templates/sourceView.html', token)

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

def printDir(request):
	fileType = []

	operation = request.POST.get('operation', '')
	directoryName = request.POST.get('dirName', '') # Get directory Name
	directoryName = nomalize_directory_path(directoryName)

	if operation == 'ReDirect':
		folderName = request.POST.get('folder', '')
		directoryName += folderName

	elif operation == 'GoBack':
		if directoryName[-1] == '/':
			directoryName = directoryName[:-1]

		index = len(directoryName) - 1
		while index > 0:
			if directoryName[index] == '/':
				break
			index = index - 1
		directoryName = directoryName[:index]

	elif operation == 'categorization':
		project_attr = request.POST.get('project_attribute', '')
		if project_attr == 'C_Lang':
			directoryName = directoryName.replace('\n', '')
			directoryName = directoryName.replace('\r', '')
			directoryName += '/*.c'

	command = 'ls -l ' + "'" + directoryName + "'"# for file type
	result = os.popen(command).read().split('\n')[1:-1] # except first line(due to total info for ls command) & split by '\n'
	for _type in result:
		fileType.append(_type[0])

	command = 'ls -1 ' + "'" + directoryName + "'"# for file name
	fileName = os.popen(command).read().split('\n')[:-1]

	fileInfo = make_file_info(fileType, fileName)
	token = {'fileInfo': fileInfo, 'dirName': directoryName}
	return render(request, 'coding/templates/printDir.html', token)

def make_file_info(_fileType, _fileName):
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

	return output

def nomalize_directory_path(_dirName):
	if _dirName == '': # PREVENT __EMPTY SET ERROR__
		_dirName = os.popen('pwd').read()
	if _dirName[-1] != '/': # PREVENT __DUPLICATED SLASH ERROR__
		_dirName += '/'
	_dirName = _dirName.replace('\n', '') # PRVENT __ENCODING ERROR__
	_dirName = _dirName.replace('\r', '')
	return _dirName
