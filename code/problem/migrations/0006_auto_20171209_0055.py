# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0005_problem_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='correct',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='problem',
            name='wrong',
            field=models.IntegerField(default=0),
        ),
    ]
