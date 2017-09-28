# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *

def intro(request):
	if request.method == 'GET':
		return render(request, 'terra/templates/intro.html')

def core(request):
	name = request.POST.get('your_name', '')
	return render(request, 'terra/templates/core.html', {'name': name})

def index(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('hello')
	else:
		form = NameForm()
	return render(request, 'terra/templates/index.html', {'form': form})
