# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('number', '0002_auto_20170504_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
