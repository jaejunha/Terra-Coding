# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def index(request):
        if request.method == 'GET':
                return render(request, 'index.html')

def intro(request):
	if request.method == 'GET':
		return render(request, 'intro.html')

def core(request):
	if request.method == 'GET':
		return render(request, 'core.html')



# Create your views here.
