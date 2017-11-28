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

		list_example = example.split('&')
		list_solution = solution.split('&')
		for i in range(0,len(list_example)-1):
			Solution(sNo=p,ex=list_example[i],sol=list_solution[i]).save()
	elif op == 'modify':
		no = request.POST.get('no',0)

		p = Problem.objects.filter(no = no)
		p.update(name=title)
		p.update(desc=desc)

		list_example = example.split('&')
		list_solution = solution.split('&')

		p = Problem.objects.get(no=no)
		Solution.objects.filter(sNo=p).delete()
		for i in range(0,len(list_example)-1):
			Solution(sNo=p,ex=list_example[i],sol=list_solution[i]).save()

	elif op == 'delete':
		number = request.POST.get('number', '')
		Problem.objects.get(no=number).delete()

	r = Solution.objects.all().order_by('sNo_id')
	list = []
	list_example =[]
	list_solution =[]
	problem_no = -1
	length = len(r)

	if length == 1:
		list.append((str(r[0].sNo.no),r[0].sNo.name,r[0].sNo.desc,r[0].ex,r[0].sol))
		return render(request, 'problem/templates/list.html',{'list':list})

	for i in range (0,length-1):
		list_example.append(r[i].ex)
		list_solution.append(r[i].sol)
		if (i+1) != (length-1):
			if r[i].sNo.no != r[i+1].sNo.no:
				list.append((str(r[i].sNo.no),r[i].sNo.name,r[i].sNo.desc,list_example,list_solution))
				list_example =[]
				list_solution =[]
		else:
			if r[i].sNo.no == r[i+1].sNo.no:
				list_example.append(r[i+1].ex)
				list_solution.append(r[i+1].sol)
				list.append((str(r[i+1].sNo.no),r[i+1].sNo.name,r[i+1].sNo.desc,list_example,list_solution))
			else:
				list.append((str(r[i].sNo.no),r[i].sNo.name,r[i].sNo.desc,list_example,list_solution))
				list.append((str(r[i+1].sNo.no),r[i+1].sNo.name,r[i+1].sNo.desc,r[i+1].ex,r[i+1].sol))
	return render(request, 'problem/templates/list.html',{'list':list})
