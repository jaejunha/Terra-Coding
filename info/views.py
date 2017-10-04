# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from terra.models import *

def info(request):
	result = User.objects.filter(number=request.session['number'])[0]
	context = {'name': result.name, 'number': result.number, 'school': result.school, 'major':result.major, 'grade':result.grade, 'picture':result.picture}
	return render(request, 'info/templates/index.html',context)
