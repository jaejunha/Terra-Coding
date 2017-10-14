# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    grade = models.SmallIntegerField()
    school = models.CharField(max_length=40)
    major = models.CharField(max_length=40)
    picture = models.CharField(max_length=100)
    def __str__(self):
        return self.name
