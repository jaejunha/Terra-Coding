# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('terra', '0004_auto_20171003_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
