# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-23 09:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rgbz', '0004_auto_20170921_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informatieobjecttype',
            name='informatieobjecttypeomschrijving',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]