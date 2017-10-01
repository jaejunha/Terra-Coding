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

error_list = ["Enter the ID", "Enter the Password", "Please check your input"]

def index(request):
	try:
		if request.session['sid']:
			cookies = {'JSESSIONID':request.session['sid']}
			response = requests.get(USER, cookies=cookies)
			soup = BeautifulSoup(response.text,'html.parser')
			list = soup.find_all('td')
			number = list[1].string
			name = list[2].string
			grade = list[3].string
			school = list[4].string
			major = list[5].string
			phone = list[18].string
			picture = 'http://job.ajou.ac.kr'+requests.get(PIC+number).text.split(' ')[2][5:].split('?')[0]
			context = {'number':number, 'name':name,'grade':grade,'school':school,'major':major,'phone':phone,'picture':picture}
			return render(request, 'terra/templates/index.html', context)
	except Exception:
		return render(request, 'terra/templates/index.html')

def login(request):
        return render(request, 'terra/templates/login.html')

def check(request):
	name = ''
	error = ''
	if request.method == 'POST':
		name = request.POST.get('id', '')
		pwd = request.POST.get('pwd','')
		cookies = ''
		if name == '':
			error = error_list[0]
		elif pwd == '':
			error = error_list[1]
		else:
			data = {'id': name, 'passwd': pwd, 'rememberMe': 'N', 'platformType':'A', 'deviceToken':''}
			response = requests.post(LOGIN, data=data)
			status = json.loads(response.text)['response']
			if status == 'OK':
				for c in response.cookies:
					if c.name == 'JSESSIONID':
						request.session['sid']=c.value
				return HttpResponseRedirect(reverse('index'))
			else:
				error = error_list[2]
	return render(request, 'terra/templates/login.html', {'name': name, 'error': error})

def out(request):
	request.session.flush()
	picture = ''
	return HttpResponseRedirect(reverse('index'))
