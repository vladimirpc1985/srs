# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 07:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srs', '0008_auto_20170218_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='notecard',
            name='body',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='notecard',
            name='keywords',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='notefile',
            name='body',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='notefile',
            name='keywords',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='notecard',
            name='label',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='notefile',
            name='label',
            field=models.TextField(null=True),
        ),
    ]
