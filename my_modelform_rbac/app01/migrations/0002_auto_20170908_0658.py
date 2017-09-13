# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-08 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='组名')),
            ],
        ),
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=32, verbose_name='角色名称'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.CharField(max_length=32, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=32, verbose_name='用户名'),
        ),
    ]