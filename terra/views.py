# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
import requests, json

def intro(request):
	if request.method == 'GET':
		return render(request, 'terra/templates/intro.html')

def core(request):
	if request.method == 'POST':
		name = request.POST.get('id', '')
		pwd = request.POST.get('pwd','')
		data = {'id': name, 'passwd': pwd, 'rememberMe': 'N', 'platformType':'A', 'deviceToken':''}
		response = requests.post('https://mb.ajou.ac.kr/mobile/login.json', data=data)
		status = json.loads(response.text)['response']
		if status == 'OK':
			return render(request, 'terra/templates/core.html', {'name': name})
		else:
			return render(request, 'terra/templates/index.html', {'name': name})
	return render(request, 'terra/templates/core.html')

def index(request):
	return render(request, 'terra/templates/index.html')
