# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

import os
from os.path import abspath, dirname
from subprocess import call
from django.core.urlresolvers import reverse

def get_all_c_files_name(fileList):
	output = []

	for fileName in fileList:
		extension = os.path.splitext(fileName)[1]
		if extension == '.c' or extension == '.h':
			output.append(fileName)

	return output

def do_compile_c_language(request):
	operation = request.POST.get('operation', '')
	fileName = request.POST.get('compile_file', '')
	dirName = request.POST.get('dirName', '')
	path = ''
	result = ''
	status = ''

	if dirName[-1] == '/':
		dirName = dirName[:-1]

	if operation == 'ALL': # Compile on a Project unit
		command = 'ls -1 ' + dirName
		allName = os.popen(command).read().split('\n')
		fileName_c = get_all_c_files_name(allName)

		for _file in fileName_c:
			path += (' ' + dirName + '/' + _file)

	elif operation == 'selected': # Compile on file unit
		path = do_path_concatenation(fileName, dirName)
		extension = os.path.splitext(path)[1]
		if extension != '.c':
			errMsg = "out of service format :)"
			return render(request, 'coding/templates/compile_res.html', {'result': errMsg , 'status': 'F'})

	gcc_compile_command = "gcc -o " + dirName + "/main " + path + " 2> " + dirName + "/compile_message"
	result = os.popen(gcc_compile_command).read() # executable file will be created in manage.py directory
	result = os.popen("cat " + dirName + "/compile_message").read() # show a error message

	if result == '': # which means error is none
		status = 'S'
		result = os.popen(dirName + "/main").read()
	else:
		status = 'F'

	return render(request, 'coding/templates/compile_res.html', {'result': result, 'status': status})

def createNewFile(request):
	dirName = request.POST.get('dirName', '')
	newFileName = request.POST.get('newFileName', '')

	dirName = dirName.replace('\n', '')
	dirName = dirName.replace('\r', '')

	if newFileName == '':
		newFileName = 'temp.c'

	if dirName[-1] == '/':
		path = dirName + newFileName
	else:
		path = dirName + '/' + newFileName

	f = open(path, 'w')
	f.write('')
	f.close()

	return HttpResponseRedirect('printDir')

def sourceDel(request):
	fileName = request.POST.get('selected_file', '')
	dirName = request.POST.get('dirNames', '')
	path = do_path_concatenation(fileName, dirName)

	os.popen("rm -rf " + path)
	return HttpResponseRedirect('printDir')

def sourceEdit(request):
	global editPath
	operation = request.POST.get('operation', '')

	if operation == 'Write':
		edit_data = request.POST.get('edit_data', '')
		f = open(editPath, 'w')
		f.write(edit_data)
		f.close()
		return HttpResponseRedirect('printDir')
	else:
		fileName = request.POST.get('selected_file', '')
		dirName = request.POST.get('dirNames', '')

		editPath = do_path_concatenation(fileName, dirName)

		f = open(editPath, 'r')
		file_data = f.read()
		f.close()

		return render(request, 'coding/templates/sourceEdit.html', {'returnPath': editPath, 'file_data': file_data})

def sourceView(request):

	fileName = request.POST.get('selected_file', '')
	dirName = request.POST.get('dirNames', '')
	viewPath = do_path_concatenation(fileName, dirName)

	'''  MORE FUNCTION REQUIRED!!! -- only a file can be open..	'''
	''' Text&img file's type'''
	f = open(viewPath, 'r')
	file_data = f.read()
	f.close()

	return render(request, 'coding/templates/sourceView.html', {'viewPath': viewPath, 'file_data': file_data})

def printDir(request):
	fileType = []

	operation = request.POST.get('operation', '')
	directoryName = request.POST.get('dirName', '') # Get directory Name

	if directoryName == '':
		directoryName = os.popen('pwd').read() # if input of directory is empty, set to current path

	if operation == 'ReDirect':
		folderName = request.POST.get('folder', '')
		directoryName = do_path_concatenation(folderName, directoryName)

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

	command = 'ls -l ' + directoryName # for file type
	result = os.popen(command).read().split('\n')[1:-1] # except first line(due to total info for ls command) & split by '\n'
	for _type in result:
		fileType.append(_type[0])

	command = 'ls -1 ' + directoryName # for file name
	fileName = os.popen(command).read().split('\n')[:-1]

	fileInfo = make_file_info(fileType, fileName)
	token = {'fileInfo': fileInfo, 'dirNames': directoryName}
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

	MAX = len(_fileType) - 1
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

def do_path_concatenation(fileName, dirName):

	'''<====[ EXCEPTION HANDLER ]====>'''
	if dirName == '':
		dirName = './'
	dirName = dirName.replace('\n', '')
	dirName = dirName.replace('\r', '')
	fileName = fileName.replace('\n', '')
	fileName = fileName.replace('\r', '')
	'''<============================>'''

	'''<====[ EXTRACT FILE NAME  ]====>'''
	index = len(fileName) - 1
	while index >= 0:
		if fileName[index] == ' ':
			break
		index = index - 1
	fileName = fileName[index+1:]
	'''<============================>'''

	'''<====[ EXTRACT DIRECTORY NAME ]====>'''
	if dirName != 'NULL': # when dirName is NULL, Skip this procedure.
		rootFlag = 0
		if dirName[0] == '/':
			rootFlag = 1

		dirName_ary = dirName.split('/')
		dirName = ''
		if rootFlag == 1:
			dirName = '/'

		for _in in dirName_ary:
			if _in != '':
				dirName += (_in + '/')
		path = dirName + fileName
	else:
		path = fileName
	'''<============================>'''

	return path
