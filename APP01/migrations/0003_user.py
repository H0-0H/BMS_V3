# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-31 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP01', '0002_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=24)),
            ],
        ),
    ]
