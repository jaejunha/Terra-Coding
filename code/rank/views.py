# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def rank(request):
	return render(request, 'rank/templates/index.html')

