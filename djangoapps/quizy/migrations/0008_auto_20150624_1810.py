# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0007_auto_20150621_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='variant',
            old_name='question',
            new_name='page',
        ),
    ]
