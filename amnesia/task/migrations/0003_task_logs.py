# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20170504_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='logs',
            field=models.TextField(blank=True),
        ),
    ]
