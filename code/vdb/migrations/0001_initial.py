# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-15 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_id', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now_add=True, verbose_name='Date')),
            ],
        ),
    ]