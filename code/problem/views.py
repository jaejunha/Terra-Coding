# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from models import *

@csrf_exempt
def problem(request):
	return render(request, 'problem/templates/index.html')

@csrf_exempt
def list(request):
	op = request.POST.get('op', '')
	title = request.POST.get('title', '')
	desc = request.POST.get('desc', '')
	example = request.POST.get('example', '')
	solution = request.POST.get('solution', '')
	no = Problem.objects.count()+1;

	if op == 'save':
		Problem(no=no,name=title,desc=desc).save()
		Solution(no=no,ex=example,sol=solution).save()

	result = Problem.objects.filter()
	list = []
	for r in result:
		list.append((str(r.no),r.name,r.desc))

	return render(request, 'problem/templates/list.html',{'list':list})
