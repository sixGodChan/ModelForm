# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20170908_0659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='m2m',
            field=models.ManyToManyField(to='app01.Role', verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='ug',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserGroup', verbose_name='科室'),
        ),
    ]
