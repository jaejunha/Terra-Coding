# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

import os
from os.path import abspath, dirname
from subprocess import call
from django.core.urlresolvers import reverse

def do_compile_c_language(request):
	fileName = request.POST.get('compile_file', '')
	dirName = request.POST.get('dirNames', '')

	path = do_path_concatenation(fileName, dirName)
	result = os.popen("gcc -o main " + path + " 2> compile_message").read() # executable file will be created in manage.py directory
	result = os.popen("cat compile_message").read() # show a error message

	if result == '': # which means error is none
		result = 'successfully compiled'

	return render(request, 'coding/templates/compile_res.html', {'result': result})

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

	operation = request.POST.get('operation', '')
	dirName = request.POST.get('dirName', '') # Get directory Name
	if dirName == '':
		dirName = os.popen('pwd').read() # if input of directory is empty, set to current path

	if operation == 'ReDirect':
		folderName = request.POST.get('folder', '')
		dirName = do_path_concatenation(folderName, dirName)

	elif operation == 'GoBack':
		if dirName[-1] == '/':
			dirName = dirName[:-1]

		index = len(dirName) - 1
		while index > 0:
			if dirName[index] == '/':
				break
			index = index - 1

		dirName = dirName[:index]


	command = 'ls -l ' + dirName
	#result = Str2Ary_Newline(os.popen(command).read())
	result = os.popen(command).read()
	result_ary = result.split('\n')
	#fileName = take_Filename_Only(result_ary[1:])

	return render(request, 'coding/templates/printDir.html', {'resultOfDir': result_ary[1:], 'dirNames': dirName}) # Exception to first row

def Str2Ary_Newline(str_in):
	out = []
	buff = []

	for c in str_in:
		if c == '\n':
			out.append(''.join(buff))
			buff = []
		else:
			buff.append(c)
	else:
		if buff:
			out.append(''.join(buff))
	return out

def take_Filename_Only(ary_in):
	out = []
	buff = []
	index = 0
	for _in in ary_in:
		index = len(_in)
		print index
		while index >= 0:
			if _in[index-1] == ' ':
				break
			index = index - 1
		out.append(_in[index:])
	return out

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
