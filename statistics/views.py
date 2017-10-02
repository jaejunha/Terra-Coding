# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def statistics(request):
	return render(request, 'statistics/templates/index.html')

