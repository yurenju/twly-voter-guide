# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-03 09:05
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_auto_20150707_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='results',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
