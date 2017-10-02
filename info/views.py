# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def info(request):
	return render(request, 'info/templates/index.html')

