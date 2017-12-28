# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-13 17:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20171011_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 13, 17, 51, 21, 905393, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='category_list', to='blog.Category'),
        ),
    ]
