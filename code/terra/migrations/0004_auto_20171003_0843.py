# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 08:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terra', '0003_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='user',
            name='picture',
        ),
    ]
