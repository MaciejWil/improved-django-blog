# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-15 09:01
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20171015_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 15, 9, 1, 56, 502280, tzinfo=utc)),
        ),
    ]