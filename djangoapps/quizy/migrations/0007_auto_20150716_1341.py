# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0006_auto_20150711_2346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonenroll',
            old_name='result',
            new_name='data',
        ),
    ]
