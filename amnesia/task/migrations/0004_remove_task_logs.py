# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 08:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_task_logs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='logs',
        ),
    ]