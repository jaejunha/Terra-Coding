# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import *
from bs4 import BeautifulSoup
import requests, json
import random

import hashlib # be used for Directory Name Hashing because of basic level security
import os # be used for popen

LOGIN = 'https://mb.ajou.ac.kr/mobile/login.json'
USER = 'https://mb.ajou.ac.kr/mobile/M03/M03_010_010.es'
PIC = 'http://job.ajou.ac.kr/office/Teacher/Per/PerPic.aspx?pid='

error_list = ["Enter the ID", "Enter the Password", "Please check your input"]

def index(request):
	if request.POST.get('intro','')=='1':
		return render(request, 'terra/templates/index.html',{'intro':'1'})
	try:
		if request.session['sid']:
			print request.session['sid']
			if request.session['sid'] == 'root':
				return render(request, 'terra/templates/index.html')
			cookies = {'JSESSIONID':request.session['sid']}
			response = requests.get(USER, cookies=cookies)
			soup = BeautifulSoup(response.text,'html.parser')
			list = soup.find_all('td')
			number = list[1].string
			request.session['number'] = number
			User(number=request.session['number'],name=list[2].string,grade=list[3].string[0],school=list[4].string,major=list[5].string,picture=('http://job.ajou.ac.kr'+(requests.get(PIC+number).text.split(' ')[2][5:].split('?')[0]))).save()
			return render(request, 'terra/templates/index.html')
	except Exception as e:
		print(e)
		request.session.flush()
		return render(request, 'terra/templates/index.html')

def login(request):
    return render(request, 'terra/templates/login.html')

def about(request):
	return render(request, 'terra/templates/about.html')

def check(request):
	name = ''
	error = ''
	if request.method == 'POST':
		name = request.POST.get('id', '')
		pwd = request.POST.get('pwd','')
		cookies = ''
		if name == 'root' and pwd=='terra1234':
			request.session['number']=999999999
			request.session['sid']='root'
			return HttpResponseRedirect(reverse('index'))
		if name == '':
			error = error_list[0]
		elif pwd == '':
			error = error_list[1]
		else:
			data = {'id': name, 'passwd': pwd, 'rememberMe': 'N', 'platformType':'A', 'deviceToken':''}
			response = requests.post(LOGIN, data=data)
			status = json.loads(response.text)['response']
			if status == 'OK':
				checkUserDirectory(request)
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

def checkUserDirectory(request):
	hash_object = hashlib.sha1(request.POST.get('id', ''))
	hex_dig = hash_object.hexdigest()
	request.session['Directory'] = hex_dig

	result = os.popen("ls -1 userDirectory | grep "+hex_dig).read()
	result = result.replace('\n', '')
	result = result.replace('\r', '')

	if result != hex_dig:
		os.popen("mkdir userDirectory").read()
		os.popen("cd userDirectory && mkdir "+hex_dig)

	return
