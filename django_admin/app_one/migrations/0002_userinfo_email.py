# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-06 08:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
