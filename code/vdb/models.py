# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import date

class VDB(models.Model):
    owner_id = models.CharField(max_length=50)
    def __str__(self):
        return self.owner_id
