# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 16:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terra', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Feedback',
        ),
    ]