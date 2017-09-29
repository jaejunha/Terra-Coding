# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import *
import requests, json

def intro(request):
	if request.method == 'GET':
		return render(request, 'terra/templates/intro.html')

def core(request):
	name = ''
	if request.method == 'POST':
		name = request.POST.get('id', '')
		pwd = request.POST.get('pwd','')
		if name != '' and pwd !='':
			data = {'id': name, 'passwd': pwd, 'rememberMe': 'N', 'platformType':'A', 'deviceToken':''}
			response = requests.post('https://mb.ajou.ac.kr/mobile/login.json', data=data)
			status = json.loads(response.text)['response']
			if status == 'OK':
				return render(request, 'terra/templates/core.html', {'name': name})
	return HttpResponseRedirect(reverse('index'))
def index(request):
	return render(request, 'terra/templates/index.html')
