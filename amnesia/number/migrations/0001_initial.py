# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('code', models.CharField(max_length=2, unique=True)),
                ('calling_code', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('area_code', models.CharField(blank=True, max_length=5)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to='number.Country')),
            ],
        ),
    ]
