# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def problem(request):
	return render(request, 'problem/templates/index.html')
