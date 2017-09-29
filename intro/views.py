# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def intro(request):
        if request.method == 'GET':
                return render(request, 'intro/templates/intro.html')


# Create your views here.
