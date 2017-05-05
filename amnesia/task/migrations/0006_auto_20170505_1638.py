# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-05 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_auto_20170505_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='every',
            field=models.CharField(choices=[('*', 'every minute'), ('*/15', '15 minutes'), ('*/30', '30 minutes'), ('0', '60 minutes')], default='0', help_text='Repeat every', max_length=4),
        ),
    ]
