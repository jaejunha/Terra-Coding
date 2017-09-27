# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
# Create your models here.
