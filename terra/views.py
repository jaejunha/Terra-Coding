# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def index(request):
        if request.method == 'GET':
                return render(request, 'index.html')


# Create your views here.
