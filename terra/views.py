# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from .forms import FeedbackForm

def create(request):
	if request.method == 'POST':
		form = FeedbackForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('/core')
	else:
		form = FeedbackForm()
	return render(request, 'core.html', {'form':form})

def index(request):
        if request.method == 'GET':
                return render(request, 'index.html')

def intro(request):
	if request.method == 'GET':
		return render(request, 'intro.html')

def core(request):
	if request.method == 'GET':
		return render(request, 'core.html')



# Create your views here.
