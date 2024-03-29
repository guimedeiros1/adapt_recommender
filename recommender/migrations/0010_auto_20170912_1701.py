# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 20:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0009_auto_20170912_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='benefits',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='objectives',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='problems',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='rationale',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
