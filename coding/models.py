# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class ProjectInfo(models.Model):
    student_number = models.CharField(max_length = 10)
    student_name = models.CharField(max_length = 30)
    private_directory = models.CharField(max_length = 150)

    def __str__(self):
        return self.student_number
