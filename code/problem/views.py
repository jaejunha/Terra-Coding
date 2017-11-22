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
		p = Problem.objects.get(no=no)
		Solution(sNo=p,ex=example,sol=solution).save()
	elif op == 'modify':
		no = request.POST.get('no',0)

		p = Problem.objects.filter(no = no)
		p.update(name=title)
		p.update(desc=desc)

		s = Solution.objects.filter(sNo=p)
		s.update(ex=example)
		s.update(sol=solution)

	elif op == 'delete':
		number = request.POST.get('number', '')
		Problem.objects.get(no=number).delete()

	result = Solution.objects.all()
	list = []
	for r in result:
		print r.sNo.desc
		list.append((str(r.sNo.no),r.sNo.name,r.sNo.desc,r.ex,r.sol))

	return render(request, 'problem/templates/list.html',{'list':list})
