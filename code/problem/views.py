# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from models import *
from django.db.models import Max

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

	if op == 'save':
		try:
			no = Problem.objects.all().aggregate(Max('no'))['no__max']+1
		except:
			no = 1
		Problem(no=no,name=title,desc=desc).save()
		Solution(no=no,ex=example,sol=solution).save()
	elif op == 'modify':
		no = request.POST.get('no',0)

		result = Problem(no = no)
		result.name = title
		result.desc = desc
		result.save()

#		result = Solution(no=no)
	#	result.ex = example
	#	result.sol= solution
	#	result.save()

	elif op == 'delete':
		number = request.POST.get('number', '')
		Problem.objects.get(no=number).delete()
		Solution.objects.get(no=number).delete()

	result = Problem.objects.filter()
	list = []
	for r in result:
		list.append((str(r.no),r.name,r.desc))

	return render(request, 'problem/templates/list.html',{'list':list})
