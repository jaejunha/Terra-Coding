# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def feedback(request):
	return render(request, 'feedback/templates/index.html')
