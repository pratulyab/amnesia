# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_customuser_total_tasks_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='logs',
            field=models.TextField(blank=True),
        ),
    ]
