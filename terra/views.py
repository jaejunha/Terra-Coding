# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import *

def intro(request):
	if request.method == 'GET':
		return render(request, 'terra/templates/intro.html')

def core(request):
	if request.method == 'POST':
		name = request.POST.get('id', '')
		pwd = request.POST.get('pwd','')
		if name =='root' and pwd=='1234':
			return render(request, 'terra/templates/core.html', {'name': name})
		else:
			return HttpResponseRedirect(reverse('index'))
	return render(request, 'terra/templates/core.html')

def index(request):
	return render(request, 'terra/templates/index.html')
