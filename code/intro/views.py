# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def intro(request):
    request.session.flush()
    return render(request, 'intro/templates/intro.html')


# Create your views here.
