# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 21:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='user_age',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
