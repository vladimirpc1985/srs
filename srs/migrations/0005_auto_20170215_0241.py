# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 02:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('srs', '0004_directories'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Directories',
            new_name='Directory',
        ),
    ]
