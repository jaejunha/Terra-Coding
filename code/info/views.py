# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from terra.models import *
from problem.models import *

def info(request):
	try:
		result = User.objects.filter(number=request.session['number'])[0]
		context = {'name': result.name, 'number': result.number, 'school': result.school, 'major':result.major, 'grade':result.grade, 'picture':result.picture}
		return render(request, 'info/templates/index.html',context)
	except:
		#if user login as admin
		if request.session['number'] == 999999999:
			list_problem = []
			result = Problem.objects.all().order_by('no')
			for r in result:
				list_problem.append((str(r.date).split('.')[0], r.no, r.name))
			context = {'problem_counter':len(result),'list_problem':list_problem}
			return render(request, 'info/templates/index.html',context)
