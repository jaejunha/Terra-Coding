# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Feedback(models.Model):
	name = models.CharField(max_length=100)
# Create your models here.
