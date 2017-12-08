# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

import sys
sys.path.append("..")
import problem
from problem.models import *

class User(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    grade = models.SmallIntegerField()
    school = models.CharField(max_length=40)
    major = models.CharField(max_length=40)
    picture = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Solve(models.Model):
    sUser = models.ForeignKey(User, on_delete=models.CASCADE)
    wrong = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)
