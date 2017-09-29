# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

import os
from os.path import abspath, dirname
from subprocess import call
from django.core.urlresolvers import reverse

# Create your views here.
def sourceView(request):
	user_sel = _user_select
	return render(request, 'terra/templates/sourceView.html', {'user_sel': user_sel})

def printDir(request):
	global _view, _edit, _del, _use
	HttpResponseRedirect('printDir')
	dirName = request.POST.get('dirName', '') # Get directory Name

	'''<==[ when button is pushed ]==>'''
	_view = request.POST.get('view', '')
	_edit = request.POST.get('edit', '')
	_del = request.POST.get('del', '')
	_user_select = request.POST.get('user_select', '')

	if _view == "view":
		return HttpResponseRedirect('sourceView')
	elif _edit:
		print '@@_eidt selected_@'
	elif _del:
		print '@@_del selected_@'
	else:
		print '@@_BUTTON EXCEPTION ERROR!!_@'
	'''<=[=========================]=>'''


	command = 'ls -l ' + dirName
	result = Str2Ary_Newline(os.popen(command).read())
	fileName = take_Filename_Only(result[1:])
	return render(request, 'coding/templates/printDir.html', {'resultOfDir': result[1:], 'fileNames': fileName, 'dirName': dirName}) # Exception to first row

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
		while len >= 0:
			if _in[index-1] == ' ':
				break
			index = index - 1
		out.append(_in[index:])
	return out
