# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-19 11:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ex', models.TextField()),
                ('sol', models.TextField()),
                ('no', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='problem.Problem')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([('no', 'ex', 'sol')]),
        ),
    ]