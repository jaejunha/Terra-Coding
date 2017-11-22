# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class Problem(models.Model):
    no = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.TextField(max_length=100, null = True)

    def __str__(self):
        return self.name

class Solution(models.Model):
    sNo = models.ForeignKey(Problem, on_delete=models.CASCADE)
    ex = models.TextField()
    sol = models.TextField()
