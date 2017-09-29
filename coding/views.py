# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

import os
from os.path import abspath, dirname
from subprocess import call
from django.core.urlresolvers import reverse

def sourceView(request):

	fileName = request.POST.get('selected_file', '')
	dirName = request.POST.get('dirNames', '')

	index = len(fileName) - 1
	while index >= 0:
		if fileName[index] == ' ':
			break
		index = index - 1
	fileName = fileName[index+1:]

	rootFlag = 0
	if dirName[0] == '/':
		rootFlag = 1

	dirName_ary = dirName.split('/')
	print dirName_ary
	dirName = ''
	if rootFlag == 1:
		dirName = '/'

	for _in in dirName_ary:
		if _in != '':
			dirName += (_in + '/')

	viewPath = dirName + fileName

	'''
	@ Author: InfiniteRegen
	@ Function: Get file information
	'''
	'''  MORE FUNCTION REQUIRED!!! -- only a file can be open..	'''
	''' Text&img file's type'''
	f = open(viewPath, 'r')
	file_data = f.read()
	f.close()

	return render(request, 'coding/templates/sourceView.html', {'viewPath': viewPath, 'file_data': file_data})

def printDir(request):
	#HttpResponseRedirect('printDir')

	dirName = request.POST.get('dirName', '') # Get directory Name
	command = 'ls -l ' + dirName
	result = Str2Ary_Newline(os.popen(command).read())
	fileName = take_Filename_Only(result[1:])
	print '[@@@] ===> %s' % dirName
	return render(request, 'coding/templates/printDir.html', {'resultOfDir': result[1:], 'fileNames': fileName, 'dirNames': dirName}) # Exception to first row

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
		while index >= 0:
			if _in[index-1] == ' ':
				break
			index = index - 1
		out.append(_in[index:])
	return out
