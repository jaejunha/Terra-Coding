# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-19 12:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0002_auto_20171119_1202'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([]),
        ),
    ]
