# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0009_auto_20150716_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonenroll',
            old_name='result',
            new_name='data',
        ),
    ]
