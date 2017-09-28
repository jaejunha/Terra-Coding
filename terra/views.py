# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

def intro(request):
	if request.method == 'GET':
		return render(request, 'terra/templates/intro.html')

def core(request):
	if request.method == 'POST':
		name = request.POST.get('id', '')
	return render(request, 'terra/templates/core.html', {'name': name})

def index(request):
	if request.method == 'POST':
		return HttpResponseRedirect('hello')
	return render(request, 'terra/templates/index.html')
