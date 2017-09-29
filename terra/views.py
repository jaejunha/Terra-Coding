# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import *
from bs4 import BeautifulSoup
import requests, json

LOGIN = 'https://mb.ajou.ac.kr/mobile/login.json'
USER = 'https://mb.ajou.ac.kr/mobile/M03/M03_010_010.es'
PIC = 'http://job.ajou.ac.kr/office/Teacher/Per/PerPic.aspx?pid='

def intro(request):
	if request.method == 'GET':
		return render(request, 'terra/templates/intro.html')

def core(request):
	try:
		if request.session['sid']:
			cookies = {'JSESSIONID':request.session['sid']}
			response = requests.get(USER, cookies=cookies)
			soup = BeautifulSoup(response.text,'html.parser')
			number = soup.find_all('td')[1].string
			picture = 'http://job.ajou.ac.kr'+requests.get(PIC+number).text.split(' ')[2][5:].split('?')[0]
#		for a in soup.find_all('td'):
#			print(str(a))
			return render(request, 'terra/templates/core.html', {'picture':picture})
	except Exception:
		print(request.session['sid'])

		return render(request, 'terra/templates/core.html')

def index(request):
        return render(request, 'terra/templates/index.html')

def login(request):
	name = ''
	if request.method == 'POST':
		name = request.POST.get('id', '')
		pwd = request.POST.get('pwd','')
		cookies = ''
		if name != '' and pwd !='':
			data = {'id': name, 'passwd': pwd, 'rememberMe': 'N', 'platformType':'A', 'deviceToken':''}
			response = requests.post(LOGIN, data=data)
			status = json.loads(response.text)['response']
			if status == 'OK':
				request.session.flush()
				for c in response.cookies:
					if c.name == 'JSESSIONID':
						request.session['sid']=c.value
				print(request.session['sid'])
				return HttpResponseRedirect(reverse('core'))
	return render(request, 'terra/templates/index.html', {'name': name})

