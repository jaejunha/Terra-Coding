# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

@python_2_unicode_compatible
class Post(models.Model):
	title = models.CharField('TITLE', max_length=50)
	slug = models.SlugField('SLUG', unique=True, allow_unicode=True, help_text='
