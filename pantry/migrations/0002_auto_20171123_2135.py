# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-24 02:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pantry', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='substitutefood',
            unique_together=set([('substitute_food', 'substitution')]),
        ),
    ]
